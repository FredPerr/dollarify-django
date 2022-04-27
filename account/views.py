from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import (
    LoginView, LogoutView, 
    PasswordChangeView, PasswordResetView,
    PasswordChangeDoneView as PCD,
    PasswordResetConfirmView
)

from .models import User
from .forms import (
    UserRegisterForm, UserEditForm, UserConnectForm, 
    UserPasswordChangeForm, UserRecoverForm,
    UserPasswordSetForm
)



class RegisterView(generic.CreateView):
    form_class = UserRegisterForm
    success_url = reverse_lazy("auth-overview")
    template_name = "account/register.html"


class ConnectView(LoginView):
    form_class = UserConnectForm
    success_url = reverse_lazy("auth-overview")
    template_name = "account/connect.html"
    redirect_authenticated_user = True


class DisconnectView(LogoutView):
    template_name = "account/disconnect.html"


class EditView(generic.UpdateView):
    model = User
    form_class = UserEditForm
    success_url = reverse_lazy("auth-overview")
    template_name = "account/edit.html"


class PasswordEditView(PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("auth-password-change-done")
    template_name = "account/password/change.html"
    title = "Password change"


class PasswordRecoverView(PasswordResetView):
    email_template_name = "account/password/reset-email.html"
    # extra_email_context = None
    form_class = UserRecoverForm
    # from_email = None
    # html_email_template_name = None
    subject_template_name = "account/password/reset-email-subject.txt"
    success_url = reverse_lazy("auth-recover-done")
    template_name = "account/password/recover.html"
    # title = _("Password reset")
    # token_generator = default_token_generator


@login_required
def overview(request):
    return render(request, 'account/overview.html')


class PasswordResetView(PasswordResetConfirmView):
    form_class = UserPasswordSetForm
    success_url = reverse_lazy("auth-recover-complete")
    template_name = "account/password/reset.html"


class PasswordChangeDone(PCD):
    template_name = "account/password/change-done.html"

    
def password_recover_done(request):
    return render(request, 'account/password/recover-done.html')


def password_reset_complete(request):
    return render(request, 'account/password/reset-complete.html')