from abc import abstractmethod
import pandas as pd
import os
import time
from io import BytesIO

from pandas.core.base import NoNewAttributesMixin
from azure.storage.blob import BlobServiceClient,  __version__

#from dummit.dummit_factories import LocationFactory

from dummit.dummit_tests import TestResult
from dummit.dummit_secrets import AzureSecretsManager
from . import dummit_tests as dt
from . import dummit_df_tests as dft
from . import dummit_factories as df

class MethodNotImplementedException(Exception):
    pass

class UnableToLoadFormatToPandas(Exception):
    pass

class Input():
    """
    Generic Input class that definess all the Tests we expect subclasses to implement
    It actually handles the DataFrame Tests as the specialized class: File / AzureBlob / OracleTable will 
        be there to support it with the DataFrame and placing that logic here makes less duplication (I think :))
    """
    def __init__(self,data_dict):
        # common fields 
        self.name = data_dict.get("input_name")
        self.type = data_dict.get("input_type")
        self.format = data_dict.get("input_format", "csv")
        self.header_row = data_dict.get("input_header_row", True)
        self._df = None # filled via getDataFrame not to recreate it for each test
        self.testRunID = None   # a non yaml field, to be used to ensure 
                                # local storage is in unique location for the current test run
                                # so its not downloaded only once
        self.location = df.LocationFactory.createLocationFromDict(data_dict["input_location"])
    
    @abstractmethod
    def getDataFrame(self,format:str):
        raise MethodNotImplementedException("in getDataFrame")

    @abstractmethod
    def runPresenceTest(self) -> TestResult :
        raise MethodNotImplementedException("in runPresenceTest")

    @abstractmethod
    def runFreshEnoughTest(self, test:dt.FreshEnoughTest) -> TestResult :
        raise MethodNotImplementedException("in runFreshEnoughTest")

    def runUniquenessTest(self, test:dt.FormatTest) -> TestResult :
        df = None
        df = self.getDataFrame() 
        if type(df) != pd.DataFrame:
            return dt.TestResult.COMPLETED_WITH_FAILURE
        else:
            return dft.DataFrameTester.testForUniqueness(df,test)

    def runFormatTest(self,  test:dt.FormatTest) -> TestResult :
        df = None
        df = self.getDataFrame() 
        if type(df) != pd.DataFrame:
            return dt.TestResult.COMPLETED_WITH_FAILURE
        else:
            return dft.DataFrameTester.testForFormat(df,test)

    def __str__(self):
        msg = f"Input Name: '{self.name}', Input Type: '{self.type}', Location: {self.location}"
        return msg

class LocalFileInput(Input):
    """
    A file accessible through file system. Actualy a network mount shall also work here.
    """
    def __init__(self,data_dict):
        super().__init__(data_dict)
    
    def getDataFrame(self):
        if self.runPresenceTest() == TestResult.COMPLETED_WITH_FAILURE:
            return None
        if type(self._df)!=pd.DataFrame:
            format = self.format.lower()
            if format=="excel" or format =="xls" or format=="xlsx":
                self._df = pd.read_excel(self.location.getLocationString())
            elif format=="csv":
                self._df = pd.read_csv(self.location.getLocationString())
            elif format=="paruqet":
                self._df = pd.read_parquet(self.location.getLocationString())
            else:
                raise UnableToLoadFormatToPandas(f"{format} is a bit of a stranger to me.")
        return self._df
        
    def runPresenceTest(self) -> TestResult :
        path = self.location.getLocationString()    
        if os.path.isfile(path):
            return TestResult.COMPLETED_WITH_SUCCESS
        else:
            return TestResult.COMPLETED_WITH_FAILURE

    def runFreshEnoughTest(self, test: dt.FreshEnoughTest) -> TestResult :
        """ Checks last modification date (and if file exist as well, only if it exist a concept of modification data is there. """
        path = self.location.getLocationString()
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
    def __init__(self,data_dict):
        super().__init__(data_dict)
    
    def runPresenceTest(self) -> dt.TestResult :
        properties = self.getBlobProperties()
        if properties:
            return TestResult.COMPLETED_WITH_SUCCESS
        else:
            return TestResult.COMPLETED_WITH_FAILURE
    
    def runFreshEnoughTest(self, test: dt.FreshEnoughTest) -> TestResult :
        properties = self.getBlobProperties()
        if properties:
            return TestResult.COMPLETED_WITH_SUCCESS
        else:
            return TestResult.COMPLETED_WITH_FAILURE
        

    def getBlobProperties(self):
        #1. Get all login params
        connection_details = self.location.parseAsAzureLocation()
        key_vault_name = self.secrets_location
        secret_name = connection_details["keyvault_secret_name"]
        conn_string = AzureSecretsManager.getSecretValueByName(key_vault_name, secret_name)
        blob_service_client = BlobServiceClient.from_connection_string(conn_string)
        #2. Check if blob is there
        container = connection_details["storage_container"]
        blob = connection_details["storage_blob"]
        blob_client = blob_service_client.get_blob_client(container,blob)
        try:
            return blob_client.get_blob_properties()
        except:
            return None
    
    def getBlobContentBytes(self):
         #1. Get all login params
        connection_details = self.location.parseAsAzureLocation()
        key_vault_name = self.secrets_location
        secret_name = connection_details["keyvault_secret_name"]
        conn_string = AzureSecretsManager.getSecretValueByName(key_vault_name, secret_name)
        blob_service_client = BlobServiceClient.from_connection_string(conn_string)
        #2. Check if blob is there
        container = connection_details["storage_container"]
        blob = connection_details["storage_blob"]
        blob_client = blob_service_client.get_blob_client(container,blob)
        try:
            return blob_client.download_blob().readall()
        except:
            return None
        
    def getDataFrame(self):
        if self.runPresenceTest() == TestResult.COMPLETED_WITH_FAILURE:
            return None
        if type(self._df)!=pd.DataFrame:
            format = self.format.lower()
            if format=="excel" or format =="xls" or format=="xlsx":
                self._df = pd.read_excel(BytesIO(self.getBlobContentBytes()))
            elif format=="csv":
                self._df = pd.read_csv(BytesIO(self.getBlobContentBytes()))
            elif format=="paruqet":
                self._df = pd.read_parquet(BytesIO(self.getBlobContentBytes()))
            else:
                raise UnableToLoadFormatToPandas(f"{format} is a bit of a stranger to me.")
        return self._df

        
    
class OracleTableInput(Input):
    """
    It does not exist for real. At least not yet. But why not test some Table for compliance?
    Need to think about caching the query result during test run
    """
    def __init__(self,data_dict):
        super().__init__(data_dict)

class SharepointBlobInput(Input):
    """ nothing here yet"""
    def __init__(self,data_dict):
        super().__init__(data_dict)