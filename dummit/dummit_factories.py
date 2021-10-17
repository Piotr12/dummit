from . import dummit_inputs as di
from . import dummit_tests as dt
from . import dummit_locations as dl

class UnknownInputTypeException(Exception):
    pass

class UnknownTestTypeException(Exception):
    pass

class UnknownLocationTypeException(Exception):
    pass

class InputFactory():
    @staticmethod
    def createInputFromDict(environments,data_dict):
        input_type = data_dict.get("input_type")
        if input_type=="local_file":
            return di.LocalFileInput(environments,data_dict)
        else:
            raise UnknownInputTypeException(input_type)

class TestFactory():
    @staticmethod
    def createTestFromDict(environments,data_dict):
        test_type = data_dict.get("test_type")
        if test_type=="presence_test":
            return dt.PresenceTest(data_dict)
        elif test_type=="fresh_enough_test":
            return dt.FreshEnoughTest(data_dict)
        elif test_type=="format_test":
            return dt.FormatTest(data_dict)
        elif test_type=="uniqueness_test":
            return dt.UniquenessTest(data_dict)
        else:
            raise UnknownTestTypeException(test_type)

class LocationFactory():
    @staticmethod
    def createLocationFromDict(environments,data_dict):
        location_type = data_dict.get("location_type")
        if location_type=="exact_location":
            pass
        elif location_type=="":
            pass
        else:
            raise UnknownLocationTypeException(location_type)