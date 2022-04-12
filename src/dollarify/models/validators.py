import re

def validate_min_max(value, min, max) -> bool:    
    if max is not None and value > max:
        return False
    if min is not None and value < min:
        return False
    return True

def assert_min_max(type_: type, min, max):
    # assert max is None or isinstance(min, type_.__class__), f"The maximum parameter should be set to None or {str(type_)}."
    # assert min is None or isinstance(min, type_), f"The minimum parameter should be set to None or {str(type_)}."
    if max is not None and min is not None:
        assert max > min, "The maximum should be greater than the minimum value for the parameter min and max."


def validate_uuid(value) -> bool:
    return len(value) == 32
    

def validate_username(username) -> bool:
    return re.match("^[a-zA-Z0-9_.-]+$", username) is not None