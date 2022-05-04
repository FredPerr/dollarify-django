from django.urls import path
from .views import home


urlpatterns = [
    path('', home, name='dashboard'),

    # path('account/', account, name='dashboard-account'),
    # path('account/create', account_create, name='dashboard-account-create'),
    # path('account/<uuid:id>/', account, name='dashboard-account'),

    # path('entity/', financial_entity, name='dashboard-financial-entity'),
    # path('entity/create', financial_entity_create, name='dashboard-financial-entity-create'),
    # path('entity/<uuid:id>/', financial_entity, name='dashboard-financial-entity'),

    # path('trading/<uuid:id>/', financial_entity, name='dashboard-financial-entity'),    
]