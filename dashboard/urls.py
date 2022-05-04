from django.urls import path
from .views import StockMarketAccountDetailView, home, StockMarketAccountCreateView, StockMarketAccountDeleteView


app_name = 'dashboard'


urlpatterns = [
    path('', home, name='dashboard'),

    path('account/stock-market/create/', StockMarketAccountCreateView.as_view(), name='stock-market-account-create'),
    path('account/stock-market/<uuid:id>/', StockMarketAccountDetailView.as_view(), name='stock-market-account-detail'),
    path('accout/stock-market/delete/<uuid:id>/', StockMarketAccountDeleteView.as_view(), name='stock-market-account-remove')

    # path('account/', account, name='dashboard-account'),
    # path('account/create', account_create, name='dashboard-account-create'),
    # path('account/<uuid:id>/', account, name='dashboard-account'),

    # path('entity/', financial_entity, name='dashboard-financial-entity'),
    # path('entity/create', financial_entity_create, name='dashboard-financial-entity-create'),
    # path('entity/<uuid:id>/', financial_entity, name='dashboard-financial-entity'),

    # path('trading/<uuid:id>/', financial_entity, name='dashboard-financial-entity'),    
]