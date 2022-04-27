from django.urls import path

from .views import (
    EditView, RegisterView, ConnectView, 
    DisconnectView, PasswordEditView, PasswordRecoverView, 
    overview, PasswordChangeDone, password_recover_done, PasswordResetView,
    password_reset_complete
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth-registration'),
    path('connect/', ConnectView.as_view(), name='auth-connect'),
    path('disconnect/', DisconnectView.as_view(), name='auth-disconnection'),
    path('edit/', EditView.as_view(), name='auth-edit'),

    path('password/change/', PasswordEditView.as_view(), name='auth-password-change'),
    path('password/change/done/', PasswordChangeDone.as_view(), name='auth-password-change-done'),
    path('password/recover/', PasswordRecoverView.as_view(), name='auth-recover'),
    path('password/recover/done/', password_recover_done, name='auth-recover-done'),
    path('password/reset/<uidb64>/<token>/', PasswordResetView.as_view(), name='auth-reset'),
    path('password/recover/completed/', password_reset_complete, name='auth-recover-complete'),

    path('', overview, name='auth-overview'),
]