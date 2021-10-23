import re

class Location:
    def __init__(self,location_string):
        self.location_string = location_string # here some resource identifier will end
    def __str__(self):
        return self.location_string
    def getLocationString(self):
        return self.location_string
    def parseAsAzureLocation(self):
        """
        sample for what I try to parse: 
            prod_blob_connection_key@playgroundblob01/dummit/demos/products_file.dev.csv
        """
        regexp = "(.+)@([^/]+)/([^/]+)/(.+)"
        m = re.search(regexp,self.getLocationString())
        return {
            "keyvault_secret_name" : m.group(1),
            "storage_account" : m.group(2),
            "storage_container" : m.group(3),
            "storage_blob" : m.group(4)
        }

class ExactLocation(Location):
    """ Nothing extra here vs the base Location"""
    pass

class DateDrivenRegexpLocation(Location):
    """ And here a 'chicken and egg' situation occurs. Making 'PresenceTest' for those Locations a bit of a nonsense / repetition
    I will need to check for the file and update the location_string on the fly or set it to some false value that will fail the 'PresenceTest'
    """
    pass