from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from account.models import CheckingAccount, StockMarketAccount


@login_required
def home(request):
    return render(request, 'dashboard/home.html', context={
        'stock_market_accounts': StockMarketAccount.objects.filter(user=request.user.id),
        'checking_accounts': CheckingAccount.objects.filter(user=request.user.id),
    })