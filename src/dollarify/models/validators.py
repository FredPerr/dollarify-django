def validate_min_max(value, min, max) -> bool:    
    if max is not None and value > max:
        return False
    if min is not None and value < min:
        return False
    return True

def assert_min_max(type: type, min, max):
    assert max is None or type(max) is float, "The maximum parameter should be set to None or an float."
    assert min is None or type(min) is float, "The minimum parameter should be set to None or an float."
    if max is not None and min is not None:
        assert max > min, "The maximum should be greater than the minimum value for the parameter min and max."
    