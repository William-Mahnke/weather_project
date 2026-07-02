class DateMissingError(Exception):
    """Raised if dates from the predefined date range are missing in the JSON response"""
    pass

class CityMismatchError(Exception):
    """Raised if cities intended in the final dataset are missing or an extra city is added"""
    pass

class IncompleteSeriesError(Exception):
    """Raised if number of records for each a city isn't what's expected"""