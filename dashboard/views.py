from logging import Logger
import logging
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from account.models import Account, FinancialEntity, StockMarketTrade, Transaction
from .forms import AccountCreateForm, FinancialEntityCreateForm


@login_required
def home(request):

    stock_market_accounts = Account.objects.filter(type__short_name='STOCK')

    return render(request, 'dashboard/home.html', context={
        'stock_market_accounts': stock_market_accounts
    })


@login_required
def financial_entity(request, id=None):

    if id is None:
        return render(request, 'dashboard/entity/index.html', context={
            'entities': FinancialEntity.objects.filter(account__type__isnull=True)
        })
    try:
        Account.objects.get(id=id)
        return redirect('dashboard-account', id=id)
    except Account.DoesNotExist:
        pass
    try:
        entity = FinancialEntity.objects.get(id=id)
    except FinancialEntity.DoesNotExist:
        entity = None
    
    context = {}
    if entity is not None:
        context['entity'] = entity
    return render(request, 'dashboard/entity/view.html', context=context)

@login_required
def account_create(request):
    if request.method == 'GET':
        create_form = AccountCreateForm()
        
        return render(request, 'dashboard/account/create.html', context={
            'form': create_form
        })
    elif request.method == 'POST':
        form = AccountCreateForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect('dashboard-account', id=instance.id)


@login_required
def financial_entity_create(request):
    if request.method == 'GET':
        create_form = FinancialEntityCreateForm()
        return render(request, 'dashboard/entity/create.html', context={
            'form': create_form
        })
    elif request.method == 'POST':
        form = FinancialEntityCreateForm(request.POST)
        if form.is_valid():
            instance = form.save()
            return redirect('dashboard-financial-entity', id=instance.id)
    


@login_required
def account(request, id=None):
        
    if id is not None:
        account = Account.objects.get(id=id)
        if account is None:
            id = None
        else:
            account = Account.objects.get(id=id)
            transactions = Transaction.objects.filter(Q(source_entity=account) | Q(destination_entity=account))
            return render(request, 'dashboard/account/view.html', context={
                'account': account,
                'transactions': transactions[:50],
                'total_transactions': len(transactions)
            })
    if id is None:
        return render(request, 'dashboard/account/index.html', context={
            'accounts': Account.objects.filter(user=request.user)
        })


@login_required
def stock_market_account(request):
    return render(request, 'dashboard/account/stock_market/view.html', context={
        'transactions': StockMarketTrade.objects.filter(source_entity__id=request.user.id)
    })
