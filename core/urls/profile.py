from django.urls import path


from ..views.profile import EditView, profile_overview


app_name = 'profile'


urlpatterns = [
    path('', profile_overview, name='overview'),
    path('edit/', EditView.as_view(), name='edit'),
]