import re

def validate_phone_number(value):
    return re.match("^\(?([0-9]{3})\)?[-.●]?([0-9]{3})[-.●]?([0-9]{4})$", value) is not None
