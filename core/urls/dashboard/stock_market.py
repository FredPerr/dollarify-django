from django.urls import path

from ...views.dashboard import (
    StockMarketAccountCreateView, StockMarketAccountDetailView,
    StockMarketAccountDeleteView, StockMarketNewTradeView, 
    import_trades_view, StockMarketDelTradeView,
    StockMarketEditTradeView
)


urlpatterns = [
    path('create/', StockMarketAccountCreateView.as_view(), name='stock-market-account-create'),
    path('<uuid:id>/', StockMarketAccountDetailView.as_view(), name='stock-market-account-detail'),
    path('delete/<uuid:id>/', StockMarketAccountDeleteView.as_view(), name='stock-market-account-remove'),
    path('<uuid:id>/new-trade/', StockMarketNewTradeView.as_view(), name='stock-market-new-trade'),
    path('<uuid:id>/import-trades/', import_trades_view, name='stock-market-import-trades'),
    path('<uuid:id>/del-trade/<pk>/', StockMarketDelTradeView.as_view(), name='stock-market-del-trade'),
    path('<uuid:id>/edit-trade/<pk>/', StockMarketEditTradeView.as_view(), name='stock-market-edit-trade'),
]