class Location:
    def __init__(self,location_string):
        self.location_string = location_string # here some resource identifier will end 
    def __str__(self):
        return self.location_string
    def get_location_string(self):
        return self.location_string

class ExactLocation(Location):
    """ Nothing extra here vs the base Location"""
    pass

class DateDrivenRegexpLocation(Location):
    """ And here a 'chicken and egg' situation occurs. Making 'PresenceTest' for those Locations a bit of a nonsense / repetition
    I will need to check for the file and update the location_string on the fly or set it to some false value that will fail the 'PresenceTest'
    """
    pass