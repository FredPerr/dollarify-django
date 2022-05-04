from django.urls import path


from ..views.auth import RegisterView, ConnectView, DisconnectView


app_name = 'auth'


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('connect/', ConnectView.as_view(), name='connect'),
    path('disconnect/', DisconnectView.as_view(), name='disconnect'),
]