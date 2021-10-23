import os
import yaml
import time
import uuid

from . import dummit_factories as df
from . import dummit_tests as dt

class ConfigUninteligibleException(Exception):
    pass

class TextLogger():
    """ Simple logging helper. 
    To be expanded with HTML one or one that stores results in DB, central log service ...
       ... or some ReportPortal whatever"""
    def logTest(self,test,message):
        print (self.timestamp(),str(test),str(message))
    def logMessage(self,message):
        print (self.timestamp(),message)
    def timestamp(self):
        return time.strftime("%d/%m/%Y %H:%M:%S %Z", time.localtime())

class TestLibrary():
    def __init__(self,yaml_string,logger:TextLogger):
        # Set the logger so I can start logging
        self.logger = logger
        self.logger.logMessage(f"Logger Started")
        
        # Load the yaml config
        config = yaml.load(yaml_string,Loader=yaml.SafeLoader)
        self.logger.logMessage("Config Loaded") 

        # Load the secrets data (provider and location for it)
        secrets = config.get("secrets",None)
        if secrets:
            self.secrets_provider = secrets.get("secrets_provider","")
            self.secrets_location = secrets.get("secrets_location","")
        # Read the yaml input
        self.name = config["name"]
        # Inputs part (tests are there within input config as well!)
        self.inputs = {}
        self.tests = []
        for input_dict in config["inputs"]:
            input = df.InputFactory.createInputFromDict(input_dict)
            if self.secrets_provider:
                input.secrets_provider = self.secrets_provider
                input.secrets_location = self.secrets_location
            self.inputs[input.name] = input
            # this double for loop section below is ... ugly :( need some redesign when time allows. 
            if "must" in input_dict:
                for critical_test in input_dict["must"]:
                    test_type = list(critical_test.keys())[0]
                    test_definition = list(critical_test.values())[0]
                    test = df.TestFactory.createTestFromDict(input.name,test_type,
                                test_definition, is_critical=True)
                    self.tests.append(test)
            if "would_be_nice_for_it_to" in input_dict:
                for nice_to_have_test in input_dict["would_be_nice_for_it_to"]:        
                    test_type = list(nice_to_have_test.keys())[0]
                    test_definition = list(nice_to_have_test.values())[0]
                    test = df.TestFactory.createTestFromDict(input.name,test_type,
                                test_definition, is_critical=False)
                    self.tests.append(test)

        self.logger.logMessage(f"Inputs count: {len(self.inputs)}")            
        self.logger.logMessage(f"Tests count: {len(self.tests)}")



        # Over an out!
        self.logger.logMessage("TestLibrary Constructor completed") 

    def run(self):
        run_uuid = uuid.uuid4()
        self.logger.logMessage(f"Running '{self.name}' Run ID {run_uuid}")
        
        # set the testRunID in the input so it has a reference where to store tmp files
        for input in self.inputs.values():
            input.testRunID = run_uuid
        # run all tests (forget parallel runs for now)
        for test in self.tests:
            test.status = dt.TestResult.IN_PROGRESS    
            if type(test) is dt.PresenceTest:
                test.status = self.inputs[test.inputName].runPresenceTest()
            elif type(test) is dt.FreshEnoughTest:
                test.status = self.inputs[test.inputName].runFreshEnoughTest(test)
            elif type(test) is dt.FormatTest:
                test.status = self.inputs[test.inputName].runFormatTest(test)
            elif type(test) is dt.UniquenessTest:
                test.status = self.inputs[test.inputName].runUniquenessTest(test)
            else:
                raise dt.UnknownTestTypeException(test.type)
            self.logger.logTest(test,test.status)
            
if __name__ == "__main__":
    with open('sample_test_library.yaml', 'r') as file:
        tests = TestLibrary(file.read(), TextLogger()) 
        tests.run()