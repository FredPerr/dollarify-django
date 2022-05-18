from django import template

from core.models import User, StockMarketAccount, IncomeAccount

register = template.Library()


@register.filter
def stock_market_accounts(value):
    if not isinstance(value, User):
        return None
    return StockMarketAccount.objects.filter(user=value.id)


@register.filter
def income_accounts(value):
    if not isinstance(value, User):
        return None
    return IncomeAccount.objects.filter(user=value.id)