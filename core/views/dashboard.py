from django.urls import reverse_lazy
from django.shortcuts import render, HttpResponseRedirect
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required


from ..models import CheckingAccount, StockMarketAccount
from ..forms import StockMarketAccountCreateForm


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
        # Edit context here.
        return context


class StockMarketAccountDeleteView(DeleteView):
    model = StockMarketAccount
    template_name = 'core/dashboard/accounts/stock_market/delete.html'
    success_url = reverse_lazy('dashboard:overview')

    pk_url_kwarg = 'id'

    def get_queryset(self):
        return super().get_queryset().filter(id=self.kwargs['id'])