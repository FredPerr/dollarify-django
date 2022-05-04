from django.urls import path, include


from ..views import home


urlpatterns = [

    path('home/', home),

    path('auth/', include('core.urls.auth')),
    path('profile/', include('core.urls.profile')),
    path('auth/password/', include('core.urls.password')),
    path('dashboard/', include('core.urls.dashboard')),
]