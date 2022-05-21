from django.urls import path


from ..views.dashboard import (
    IncomeDelPaycheckView, IncomeNewPaycheckView, IncomeSourceEntityCreateView, IncomeSourceEntityDelView, IncomeSourceEntityEditView, IncomeSourceEntityListView, StockMarketDelTradeView, StockMarketEditTradeView, StockMarketNewTradeView, dashboard_overview, StockMarketAccountCreateView, 
    StockMarketAccountDetailView, StockMarketAccountDeleteView, IncomeAccountCreateView, IncomeAccountDetailView, IncomeAccountDeleteView, import_paychecks_view,
    import_trades_view
)


app_name = 'dashboard'


urlpatterns = [
    path('', dashboard_overview, name='overview'),

    path('account/stock-market/create/', StockMarketAccountCreateView.as_view(), name='stock-market-account-create'),
    path('account/stock-market/<uuid:id>/', StockMarketAccountDetailView.as_view(), name='stock-market-account-detail'),
    path('account/stock-market/delete/<uuid:id>/', StockMarketAccountDeleteView.as_view(), name='stock-market-account-remove'),
    path('account/stock-market/<uuid:id>/new-trade/', StockMarketNewTradeView.as_view(), name='stock-market-new-trade'),
    path('account/stock-market/<uuid:id>/import-trades/', import_trades_view, name='stock-market-import-trades'),
    path('account/stock-market/<uuid:id>/del-trade/<pk>/', StockMarketDelTradeView.as_view(), name='stock-market-del-trade'),
    path('account/stock-market/<uuid:id>/edit-trade/<pk>/', StockMarketEditTradeView.as_view(), name='stock-market-edit-trade'),

    
    path('account/income/create/', IncomeAccountCreateView.as_view(), name='income-account-create'),
    path('account/income/<uuid:id>/', IncomeAccountDetailView.as_view(), name='income-account-detail'),
    path('account/income/delete/<uuid:id>/', IncomeAccountDeleteView.as_view(), name='income-account-remove'),
    path('account/income/<uuid:id>/new-paycheck/', IncomeNewPaycheckView.as_view(), name='income-new-paycheck'),
    path('account/income/<uuid:id>/new-paycheck/import-paychecks/', import_paychecks_view, name='income-import-paychecks'),
    path('account/income/<uuid:id>/del-paycheck/<pk>/', IncomeDelPaycheckView.as_view(), name='income-del-paycheck'),

    path('account/income/source/add/', IncomeSourceEntityCreateView.as_view(), name='income-source-create'),
    path('account/income/source/remove/<uuid:id>/', IncomeSourceEntityDelView.as_view(), name='income-source-delete'),
    path('account/income/source/edit/<uuid:id>/', IncomeSourceEntityEditView.as_view(), name='income-source-edit'),
    path('account/income/source/list/', IncomeSourceEntityListView.as_view(), name='income-source-list'),
]