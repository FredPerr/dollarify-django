from django.urls import reverse_lazy
from django.shortcuts import render, HttpResponseRedirect
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic.detail import DetailView


from ...models import  IncomeAccount, Paycheck
from ...forms import PaycheckCreateForm, IncomeAccountCreateForm




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