from django.urls import path


from ..views.dashboard import (
    StockMarketDelTradeView, StockMarketNewTradeView, dashboard_overview, StockMarketAccountCreateView, 
    StockMarketAccountDetailView, StockMarketAccountDeleteView
)


app_name = 'dashboard'


urlpatterns = [
    path('', dashboard_overview, name='overview'),

    path('account/stock-market/create/', StockMarketAccountCreateView.as_view(), name='stock-market-account-create'),
    path('account/stock-market/<uuid:id>/', StockMarketAccountDetailView.as_view(), name='stock-market-account-detail'),
    path('account/stock-market/delete/<uuid:id>/', StockMarketAccountDeleteView.as_view(), name='stock-market-account-remove'),

    path('account/stock-market/<uuid:id>/new-trade/', StockMarketNewTradeView.as_view(), name='stock-market-new-trade'),
    path('account/stock-market/<uuid:id>/del-trade/<pk>/', StockMarketDelTradeView.as_view(), name='stock-market-del-trade'),
]