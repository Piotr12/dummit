from dummit_inputs import *
from dummit_tests import *

class UnknownInputTypeException(Exception):
    pass

class UnknownTestTypeException(Exception):
    pass

class InputFactory():
    @staticmethod
    def createInputFromDict(environments,data_dict):
        input_type = data_dict.get("input_type")
        if input_type=="local_file":
            return LocalFileInput(environments,data_dict)
        else:
            raise UnknownInputTypeException(input_type)

class TestFactory():
    @staticmethod
    def createTestFromDict(environments,data_dict):
        test_type = data_dict.get("test_type")
        if test_type=="presence_test":
            return PresenceTest(data_dict)
        elif test_type=="fresh_enough_test":
            return FreshEnoughTest(data_dict)
        elif test_type=="format_test":
            return FormatTest(data_dict)
        else:
            raise UnknownTestTypeException(test_type)