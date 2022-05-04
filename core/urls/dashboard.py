from django.urls import path


from ..views.dashboard import (
    dashboard_overview, StockMarketAccountCreateView, 
    StockMarketAccountDetailView, StockMarketAccountDeleteView
)


app_name = 'dashboard'


urlpatterns = [
    path('', dashboard_overview, name='overview'),

    path('account/stock-market/create/', StockMarketAccountCreateView.as_view(), name='stock-market-account-create'),
    path('account/stock-market/<uuid:id>/', StockMarketAccountDetailView.as_view(), name='stock-market-account-detail'),
    path('accout/stock-market/delete/<uuid:id>/', StockMarketAccountDeleteView.as_view(), name='stock-market-account-remove')
]