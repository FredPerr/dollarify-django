from django.urls import path


from ..views.profile import profile_edit, profile_overview


app_name = 'profile'


urlpatterns = [
    path('', profile_overview, name='overview'),
    path('edit/', profile_edit, name='edit'),
]