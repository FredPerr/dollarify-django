from django import template


register = template.Library()


@register.filter
def significant_digits(value, min_digits=2):
    if value is None or '.' not in str(value):
        return value

    value_str = str(value)
    decimals = value_str.split('.', 1)[1]

    threshold = 0
    while value_str[-1] == '0' and len(decimals) - threshold > min_digits:
        threshold += 1
    
    return round(value, len(decimals) - threshold)
        

@register.filter
def thousands_separated(value):
    if value is None:
        return value
    
    return f'{value:,}'



