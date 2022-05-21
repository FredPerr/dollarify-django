from django.urls import path, include


from ...views.dashboard import dashboard_overview


app_name = 'dashboard'


urlpatterns = [
    path('', dashboard_overview, name='overview'),

    path('stock-market/', include('core.urls.dashboard.stock_market')),
    path('income/', include('core.urls.dashboard.income')),
]