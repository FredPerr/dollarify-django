from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def dashboard_overview(request):
    return render(request, 'core/dashboard/overview.html')