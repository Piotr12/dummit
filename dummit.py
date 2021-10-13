import yaml
import time
import uuid
from  dummit_factories import *
from dummit_inputs import *
from dummit_tests import *

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
        
        # Read the yaml input
        self.name = config["name"]
        self.environments = config["environments"]

        # Inputs part
        self.inputs = {}
        for input_dict in config["inputs"]:
            input = InputFactory.createInputFromDict(self.environments,input_dict)
            self.inputs[input.name] = input
        self.logger.logMessage(f"Inputs count: {len(self.inputs)}")

        # Tests part
        self.tests = []
        for test in config["tests"]:
            self.tests.append(TestFactory.createTestFromDict(self.environments,test))
        self.logger.logMessage(f"Tests count: {len(self.tests)}")

        # Over an out!
        self.logger.logMessage("TestLibrary Constructor completed") 

    def run(self, environment):
        run_uuid = uuid.uuid4()
        self.logger.logMessage(f"Running '{self.name}' for '{environment}' environment. Run ID {run_uuid}")
        
        # set the testRunID in the input so it has a reference where to store tmp files
        for input in self.inputs.values():
            input.testRunID = run_uuid
        # run all tests (forget parallel runs for now)
        for test in self.tests:
            test.status = TestResult.IN_PROGRESS    
            if type(test) is PresenceTest:
                test.status = self.inputs[test.inputName].runPresenceTest(environment,test)
            elif type(test) is FreshEnoughTest:
                test.status = self.inputs[test.inputName].runFreshEnoughTest(environment,test)
            elif type(test) is FormatTest:
                test.status = self.inputs[test.inputName].runFormatTest(environment,test)
            else:
                raise UnknownTestTypeException(test.type)
            self.logger.logTest(test,test.status)
            
if __name__ == "__main__":
    with open('sample_test_library.yaml', 'r') as file:
        tests = TestLibrary(file.read(), TextLogger()) 
        tests.run("DEV")
        tests.run("QA")
        tests.run("PROD")
