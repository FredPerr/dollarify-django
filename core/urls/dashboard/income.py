from django.urls import path

from ...views.dashboard import (
    IncomeAccountCreateView, IncomeAccountDetailView, 
    IncomeAccountDeleteView, IncomeNewPaycheckView, 
    import_paychecks_view, IncomeDelPaycheckView
)


urlpatterns = [
    path('create/', IncomeAccountCreateView.as_view(), name='income-account-create'),
    path('<uuid:id>/', IncomeAccountDetailView.as_view(), name='income-account-detail'),
    path('delete/<uuid:id>/', IncomeAccountDeleteView.as_view(), name='income-account-remove'),
    path('<uuid:id>/new-paycheck/', IncomeNewPaycheckView.as_view(), name='income-new-paycheck'),
    path('<uuid:id>/import-paychecks/', import_paychecks_view, name='income-import-paychecks'),
    path('<uuid:id>/del-paycheck/<pk>/', IncomeDelPaycheckView.as_view(), name='income-del-paycheck'),
]