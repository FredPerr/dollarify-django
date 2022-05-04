from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView

from ..forms import UserRegisterForm, UserConnectForm


class RegisterView(CreateView):
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

