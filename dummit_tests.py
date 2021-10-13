import enum

class IncompleteTestDefinition(Exception):
    pass

class TestResult:
    NOT_STARTED = 'NOT_STARTED'
    IN_PROGRESS = 'IN_PROGRESS'
    COMPLETED_WITH_SUCCESS = 'COMPLETED_WITH_SUCCESS'
    COMPLETED_WITH_FAILURE = 'COMPLETED_WITH_FAILURE'

class Test():
    def __init__(self,data_dict):
        """
        Default constructor, setting some optional fields and crashing is required fields are not there.
            name = test name
            inputName = reference to input
            isCritical = would it be something to stop the run? #TODO
            isSequential = shall it be run as one and only test or parallel run is ok? #TODO
        """
        self.status = TestResult.NOT_STARTED
        self.name = data_dict.get("test_name")     
        if self.name == None:
            raise IncompleteTestDefinition("test_name is missing")
        self.inputName = data_dict.get("test_input")
        if self.inputName == None:
            raise IncompleteTestDefinition(f"test_input is missing for test {self.name}")
        self.isCritical = data_dict.get("test_is_critical", False)   
        self.isSequential = data_dict.get("test_is_sequential",False)


    def __str__(self):
        return f"Test name: '{self.name}', isCritical:'{self.isCritical}', isSequential: '{self.isSequential}'"

class PresenceTest(Test):
    """That is actually a test without any extra params, parent class fields are enough"""
    def __init__(self,data_dict):
        super().__init__(data_dict)

class FreshEnoughTest(Test):
    """One extra field, acceptable max age in hours."""
    def __init__(self,data_dict):
        super().__init__(data_dict)
        self.maxAgeInHours = data_dict.get("test_max_age_in_hours")     
        if self.maxAgeInHours == None:
            raise IncompleteTestDefinition(f"test_max_age_in_hours is missing for '{self.name}' test")

class FormatTest(Test):
    """The most complex one right now, file format, starting row [numbered from 1], columns to check"""
    def __init__(self,data_dict):
        super().__init__(data_dict)
        self.fileFormat = data_dict.get("test_file_format")
        if self.fileFormat == None: 
            raise IncompleteTestDefinition(f"test_file_format is missing for '{self.name}' test")
        self.startingRow = data_dict.get("test_starting_row",1)
        self.columns = data_dict.get("test_columns")
        if self.columns == None:
            raise IncompleteTestDefinition(f"test_columns is missing for '{self.name}' test")
        if type(self.columns) != list:
            raise IncompleteTestDefinition(f"test_columns is not a list(?) for '{self.name}' test")
        if len(self.columns)==0:
            raise IncompleteTestDefinition(f"test_columns is an empty list for '{self.name}' test")