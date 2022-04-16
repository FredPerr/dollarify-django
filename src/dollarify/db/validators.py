import re

def validate_min_max(value, min, max) -> bool:    
    if max is not None and value > max:
        return False
    if min is not None and value < min:
        return False
    return True


def validate_uuid(value) -> bool:
    return len(value) == 32
    

def validate_username(username) -> bool:
    return re.match("^[a-zA-Z0-9_.-]+$", username) is not None