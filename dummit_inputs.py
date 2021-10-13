from dummit_tests import *
import os
import time

class TestTypeNotImplemented(Exception):
    pass

class Input():
    """
    Generic Input class that definess all the Tests we expect subclasses to implement
    """
    def __init__(self,environments,data_dict):
        self.name = data_dict.get("input_name")
        self.type = data_dict.get("input_type")
        self.testRunID = None  # a non yaml field, to be used to ensure any local storate is in unique location for the current test run
        self.locations = {}
        for environment in environments:
            self.locations[environment] = data_dict.get("input_locations").get(environment)

    def runPresenceTest(self,environment: str, test:PresenceTest) -> TestResult :
        raise TestTypeNotImplemented("in runPresenceTest")
    
    def runFreshEnoughTest(self,environment: str, test:FreshEnoughTest) -> TestResult :
        raise TestTypeNotImplemented("in runFreshEnoughTest")

    def runFormatTest(self, environment: str, test:FormatTest) -> TestResult :
        raise TestTypeNotImplemented("in runFormatTest")

    def __str__(self):
        msg = f"Input Name: '{self.name}', Input Type: '{self.type}', Locations: {self.locations}"
        return msg

class LocalFileInput(Input):
    """
    A file accessible through file system. Actualy a network mount shall also work here.
    """
    def __init__(self,environments,data_dict):
        super().__init__(environments,data_dict)
    
    def runPresenceTest(self, environment: str, test: PresenceTest) -> TestResult :
        path = self.locations[environment]
        if os.path.isfile(path):
            return TestResult.COMPLETED_WITH_SUCCESS
        else:
            return TestResult.COMPLETED_WITH_FAILURE

    def runFreshEnoughTest(self, environment: str, test: FreshEnoughTest) -> TestResult :
        """ Checks last modification date (and if file exist as well, only if it exist a concept of modification data is there. """
        path = self.locations[environment]
        if os.path.isfile(path):
            modification_timestamp = os.path.getmtime(path) 
            if time.time() < modification_timestamp +  60 * 60 * test.maxAgeInHours:
                return TestResult.COMPLETED_WITH_SUCCESS
            else:
                return TestResult.COMPLETED_WITH_FAILURE
        else: 
            return TestResult.COMPLETED_WITH_FAILURE

    def runFormatTest(self, environment: str, test: FormatTest) -> TestResult :
        """ Checks for format compliance. And existence as well."""
        path = self.locations[environment]
        if os.path.isfile(path):
            ### BELOW IS FAKE FOR A WHILE (no time to code :))
            return TestResult.COMPLETED_WITH_SUCCESS
        else:
            return TestResult.COMPLETED_WITH_FAILURE

class AzureBlobInput(Input):
    """
    It does not exist for real. At least not yet. Some tests can be done without download via API, some will require full access.
    Need to think about caching it for the test run duration if download happens.
    """
    def __init__(self,environments,data_dict):
        super().__init__(environments,data_dict)
    
class OracleTableInput(Input):
    """
    It does not exist for real. At least not yet. But why not test some Table for compliance?
    Need to think about caching the query result during test run
    """
    def __init__(self,environments,data_dict):
        super().__init__(environments,data_dict)

