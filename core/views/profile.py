from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import UpdateView
from django.urls import reverse_lazy

from ..models import User
from ..forms import UserEditForm


@login_required
def profile_overview(request):
    return render(request, 'core/user/overview.html')


class EditView(UpdateView):
    model = User
    form_class = UserEditForm
    success_url = reverse_lazy("profile:edit")
    template_name = "core/user/edit.html"