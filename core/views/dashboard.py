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
    template_name = 'core/dashboard/accounts/stock_market/trade/create.html'

    def get_success_url(self):
        return reverse_lazy('dashboard:stock-market-account-detail', kwargs={'id':self.kwargs['id']})
    
    def post(self, request, *args, **kwargs):
        form = StockMarketTradeCreateForm(request.POST)
        if form.is_valid():
            trade = form.save(commit=False)
            trade.source = StockMarketAccount.objects.get(id=self.kwargs['id'])
            trade.save()
            return HttpResponseRedirect(reverse_lazy('dashboard:stock-market-account-detail', kwargs={'id': self.kwargs['id']}))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['id'] = self.kwargs['id']
        return context


class StockMarketDelTradeView(DeleteView):
    model = StockTrade
    template_name = 'core/dashboard/accounts/stock_market/trade/delete.html'


    def get_success_url(self):
        return reverse_lazy('dashboard:stock-market-account-detail', kwargs={'id':self.kwargs['id']})
    

class StockMarketEditTradeView(UpdateView):
    model = StockTrade
    template_name = 'core/dashboard/accounts/stock_market/trade/edit.html'
    fields = ('ticker', 'currency', 'bought_on_date', 'bought_on_time', 'amount', 'bought_value', 'fees', 'sold_value', 'sold_on_date', 'sold_on_time')

    def get_success_url(self):
        return reverse_lazy('dashboard:stock-market-account-detail', kwargs={'id': self.kwargs['id']})


def import_trades_view(request, id):
    return render(request, 'core/dashboard/accounts/stock_market/trade/import.html')


# Income #
class IncomeAccountCreateView(CreateView):
    model = IncomeAccount
    form_class = IncomeAccountCreateForm
    template_name = 'core/dashboard/accounts/income/create.html'


    def post(self, request, *args, **kwargs):
        form = IncomeAccountCreateForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            return HttpResponseRedirect(reverse_lazy('dashboard:income-account-detail', kwargs={'id': account.id}))


class IncomeAccountDetailView(DetailView):
    model = IncomeAccount
    template_name = 'core/dashboard/accounts/income/detail.html'
    pk_url_kwarg = 'id'

    def get_queryset(self):
        return super().get_queryset().filter(id=self.kwargs['id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['paychecks'] = Paycheck.objects.filter(target__id=self.kwargs['id'])
        return context


class IncomeAccountDeleteView(DeleteView):
    model = IncomeAccount
    template_name = 'core/dashboard/accounts/income/delete.html'
    success_url = reverse_lazy('dashboard:overview')

    pk_url_kwarg = 'id'

    def get_queryset(self):
        return super().get_queryset().filter(id=self.kwargs['id'])


class IncomeNewPaycheckView(CreateView):
    model = Paycheck
    form_class = PaycheckCreateForm
    template_name = 'core/dashboard/accounts/income/paycheck/create.html'

    def get_success_url(self):
        return reverse_lazy('dashboard:income-account-detail', kwargs={'id':self.kwargs['id']})
    
    def post(self, request, *args, **kwargs):
        form = PaycheckCreateForm(request.POST)
        if form.is_valid():
            paycheck = form.save(commit=False)
            paycheck.target = IncomeAccount.objects.get(id=self.kwargs['id'])
            paycheck.save()
            return HttpResponseRedirect(reverse_lazy('dashboard:income-account-detail', kwargs={'id': self.kwargs['id']}))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['id'] = self.kwargs['id']
        return context


class IncomeDelPaycheckView(DeleteView):
    model = Paycheck
    template_name = 'core/dashboard/accounts/income/paycheck/delete.html'

    def get_success_url(self):
        return reverse_lazy('dashboard:income-account-detail', kwargs={'id':self.kwargs['id']})


def import_paychecks_view(request, id):
    return render(request, 'core/dashboard/accounts/income/paycheck/import.html')