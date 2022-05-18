from django import template

from core.models import CurrencyRate

register = template.Library()


@register.filter
def conversion_rate(value, arg):
    try:
        return CurrencyRate.objects.get(from_cur=value, to_cur=arg).rate
    except CurrencyRate.DoesNotExist:
        return f"INVALID CONVERSION: {value}/{arg}"

