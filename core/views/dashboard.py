from django.urls import reverse_lazy
from django.shortcuts import render, HttpResponseRedirect
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required


from ..models import CheckingAccount, CurrencyRate, StockMarketAccount, StockTrade
from ..forms import StockMarketAccountCreateForm, StockMarketTradeCreateForm
from .. import currency


@login_required
def dashboard_overview(request):
    return render(request, 'core/dashboard/overview.html', context={
        'stock_market_accounts': StockMarketAccount.objects.filter(user=request.user.id),
        'checking_accounts': CheckingAccount.objects.filter(user=request.user.id),
    })


class StockMarketAccountCreateView(CreateView):
    model = StockMarketAccount
    form_class = StockMarketAccountCreateForm
    template_name = 'core/dashboard/accounts/stock_market/create.html'


    def post(self, request, *args, **kwargs):
        form = StockMarketAccountCreateForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            return HttpResponseRedirect(reverse_lazy('dashboard:stock-market-account-detail', kwargs={'id': account.id}))


class StockMarketAccountDetailView(DetailView):
    model = StockMarketAccount
    template_name = 'core/dashboard/accounts/stock_market/detail.html'
    pk_url_kwarg = 'id'

    def get_queryset(self):
        return super().get_queryset().filter(id=self.kwargs['id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = context['object'].id
        # context['loans'] = Loan.objects.filter(target__id=id)
        # context['paychecks'] = Paycheck.objects.filter(target__id=id)
        # context['payments'] = Payment.objects.filter(source__id=id)
        # context['fund_transfers'] = FundTransfer.objects.filter(Q(source__id=id) | Q(target__id=id))
        context['trades'] = StockTrade.objects.filter(source__id=id)
        context['USD_to_CAD_rate'] = CurrencyRate.objects.get(from_cur='USD', to_cur='CAD').rate
        context['CAD_to_USD_rate'] = CurrencyRate.objects.get(from_cur='CAD', to_cur='USD').rate
        return context


class StockMarketAccountDeleteView(DeleteView):
    model = StockMarketAccount
    template_name = 'core/dashboard/accounts/stock_market/delete.html'
    success_url = reverse_lazy('dashboard:overview')

    pk_url_kwarg = 'id'

    def get_queryset(self):
        return super().get_queryset().filter(id=self.kwargs['id'])

class StockMarketNewTradeView(CreateView):
    model = StockTrade
    form_class = StockMarketTradeCreateForm
    template_name = 'core/dashboard/accounts/stock_market/new-trade.html'

    def get_success_url(self):
        return reverse_lazy('dashboard:stock-market-account-detail', uuid=self.kwargs['id'])
    
    def post(self, request, *args, **kwargs):
        form = StockMarketTradeCreateForm(request.POST)
        if form.is_valid():
            trade = form.save(commit=False)
            trade.source = StockMarketAccount.objects.get(id=self.kwargs['id'])
            trade.save()
            return HttpResponseRedirect(reverse_lazy('dashboard:stock-market-account-detail', kwargs={'id': self.kwargs['id']}))
