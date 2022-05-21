from django.urls import reverse_lazy
from django.shortcuts import render, HttpResponseRedirect
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required


from ..models import  CurrencyRate, IncomeAccount, Paycheck, StockMarketAccount, StockTrade
from ..forms import PaycheckCreateForm, StockMarketAccountCreateForm, StockMarketTradeCreateForm, IncomeAccountCreateForm


@login_required
def dashboard_overview(request):
    return render(request, 'core/dashboard/overview.html')
