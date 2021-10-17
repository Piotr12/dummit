import pandas as pd
import os
import time

from . import dummit_tests as dt
from . import dummit_df_tests as dft

class MethodNotImplementedException(Exception):
    pass

class UnableToLoadFormatToPandas(Exception):
    pass

class Input():
    """
    Generic Input class that definess all the Tests we expect subclasses to implement
    """
    def __init__(self,environments,data_dict):
        # common fields 
        self.name = data_dict.get("input_name")
        self.type = data_dict.get("input_type")
        self.format = data_dict.get("input_format", "csv")
        self.header_row = data_dict.get("input_header_row", True)
        self._df = None # filled via getDataFrame not to recreate it for each test
        self.testRunID = None   # a non yaml field, to be used to ensure 
                                # local storage is in unique location for the current test run
                                # so its not downloaded only once
        self.locations = {}
        for environment in environments:
            self.locations[environment] = data_dict.get("input_locations").get(environment)

    def getDataFrame(self, environment,format):
        raise MethodNotImplementedException("in getDataFrame")

    def runPresenceTest(self,environment: str) -> dt.TestResult :
        raise MethodNotImplementedException("in runPresenceTest")
    
    def runFreshEnoughTest(self,environment: str, test:dt.FreshEnoughTest) -> dt.TestResult :
        raise MethodNotImplementedException("in runFreshEnoughTest")

    def runUniquenessTest(self, environment: str, test:dt.FormatTest) -> dt.TestResult :
        df = None
        df = self.getDataFrame(environment) 
        if type(df) != pd.DataFrame:
            return dt.TestResult.COMPLETED_WITH_FAILURE
        else:
            return dft.DataFrameTester.testForUniqueness(df,test)

    def runFormatTest(self, environment: str, test:dt.FormatTest) -> dt.TestResult :
        df = None
        df = self.getDataFrame(environment) 
        if type(df) != pd.DataFrame:
            return dt.TestResult.COMPLETED_WITH_FAILURE
        else:
            return dft.DataFrameTester.testForFormat(df,test)

    def __str__(self):
        msg = f"Input Name: '{self.name}', Input Type: '{self.type}', Locations: {self.locations}"
        return msg

class LocalFileInput(Input):
    """
    A file accessible through file system. Actualy a network mount shall also work here.
    """
    def __init__(self,environments,data_dict):
        super().__init__(environments,data_dict)
    
    def getDataFrame(self,environment):
        if self.runPresenceTest(environment) == dt.TestResult.COMPLETED_WITH_FAILURE:
            return None
        if type(self._df)!=pd.DataFrame:
            format = self.format.lower()
            if format=="excel" or format =="xls" or format=="xlsx":
                self._df = pd.read_excel(self.locations[environment])
            elif format=="csv":
                self._df = pd.read_csv(self.locations[environment])
            elif format=="paruqet":
                self._df = pd.read_parquet(self.locations[environment])
            else:
                raise UnableToLoadFormatToPandas(f"{format} is a bit of a stranger to me.")
        return self._df
        
    def runPresenceTest(self, environment: str) -> dt.TestResult :
        path = self.locations[environment]
        if os.path.isfile(path):
            return dt.TestResult.COMPLETED_WITH_SUCCESS
        else:
            return dt.TestResult.COMPLETED_WITH_FAILURE

    def runFreshEnoughTest(self, environment: str, test: dt.FreshEnoughTest) -> dt.TestResult :
        """ Checks last modification date (and if file exist as well, only if it exist a concept of modification data is there. """
        path = self.locations[environment]
        if os.path.isfile(path):
            modification_timestamp = os.path.getmtime(path) 
            if time.time() < modification_timestamp +  60 * 60 * test.maxAgeInHours:
                return dt.TestResult.COMPLETED_WITH_SUCCESS
            else:
                return dt.TestResult.COMPLETED_WITH_FAILURE
        else: 
            return dt.TestResult.COMPLETED_WITH_FAILURE


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

