from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import UpdateView
from django.urls import reverse_lazy


from ..models import User
from ..forms import UserEditForm


@login_required
def profile_overview(request):
    return render(request, 'core/user/overview.html')


@login_required
def profile_edit(request):
    

    form = UserEditForm(instance=request.user)
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile:overview')

    return render(request, 'core/user/edit.html', context={
        'form': form
    })
