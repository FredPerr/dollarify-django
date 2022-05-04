from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import render, HttpResponseRedirect
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import (
    LoginView, LogoutView, 
    PasswordChangeView, PasswordResetView,
    PasswordChangeDoneView as PCD,
    PasswordResetConfirmView
)

from .models import User, CheckingAccount, StockMarketAccount
from .forms import (
    UserRegisterForm, UserEditForm, UserConnectForm, 
    UserPasswordChangeForm, UserRecoverForm,
    UserPasswordSetForm, StockMarketAccountCreateForm
)


class RegisterView(generic.CreateView):
    form_class = UserRegisterForm
    success_url = reverse_lazy("dashboard:overview")
    template_name = "core/user/auth/register.html"


class ConnectView(LoginView):
    form_class = UserConnectForm
    success_url = reverse_lazy("dashboard:overview")
    template_name = "core/user/auth/connect.html"
    redirect_authenticated_user = True


class DisconnectView(LogoutView):
    template_name = "core/user/auth/disconnect.html"


class EditView(generic.UpdateView):
    model = User
    form_class = UserEditForm
    success_url = reverse_lazy("profile:edit")
    template_name = "core/user/edit.html"


class PasswordEditView(PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("password:change-done")
    template_name = "core/user/password/change.html"
    title = "Password change"


class PasswordRecoverView(PasswordResetView):
    email_template_name = "core/user/password/reset-email.html"
    # extra_email_context = None
    form_class = UserRecoverForm
    # from_email = None
    # html_email_template_name = None
    subject_template_name = "core/user/password/reset-email-subject.txt"
    success_url = reverse_lazy("password:recover-done")
    template_name = "core/user/password/recover.html"
    # title = _("Password reset")
    # token_generator = default_token_generator


@login_required
def profile_overview(request):
    return render(request, 'core/user/overview.html')


class PasswordResetView(PasswordResetConfirmView):
    form_class = UserPasswordSetForm
    success_url = reverse_lazy("password:recover-complete")
    template_name = "core/user/password/reset.html"


class PasswordChangeDone(PCD):
    template_name = "core/user/password/change-done.html"

    
def password_recover_done(request):
    return render(request, 'core/user/password/recover-done.html')


def password_reset_complete(request):
    return render(request, 'core/user/password/reset-complete.html')


# Account views #
@login_required
def dashboard_home(request):
    return render(request, 'core/dashboard/home.html', context={
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