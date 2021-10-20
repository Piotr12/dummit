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
    def createInputFromDict(data_dict):
        input_type = data_dict.get("input_type")
        if "local_file" in input_type:
            return di.LocalFileInput(data_dict)
        else:
            raise UnknownInputTypeException(input_type)

class TestFactory():
    @staticmethod
    def createTestFromDict(input_name,test_type, test_definition, is_critical=False):
        if test_type=="be_present":
            return dt.PresenceTest(input_name,is_critical) # test definition is a dummy here 
        elif test_type=="be_modified_at_least_x_hours_ago":
            return dt.FreshEnoughTest(input_name,test_definition,is_critical)
        elif test_type=="be_well_formated":
            return dt.FormatTest(input_name,test_definition,is_critical)
        elif test_type=="have_no_duplicates_for_a_key_of":
            return dt.UniquenessTest(input_name,test_definition,is_critical)
        else:
            raise UnknownTestTypeException(test_type)

class LocationFactory():
    @staticmethod
    def createLocationFromDict(data_string):
        values = data_string.split(",")
        location_type = values[0].replace(" ","")
        location_value = values[1].replace(" ","")
        if location_type=="exact":
            return dl.ExactLocation(location_value)
            pass
        elif location_type=="":
            pass
        else:
            raise UnknownLocationTypeException(location_type)