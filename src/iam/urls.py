from django.urls import path

from iam.views.login_view import LoginView
from iam.views.refreshtoken_view import RefreshTokenView
from iam.views.confirm_email_view import ConfirmationEmailView
from iam.views.reset_password_view import ResetPasswordView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('refresh/', RefreshTokenView.as_view(), name='refresh-token'),
    path('confirm-email', ConfirmationEmailView.as_view(), name='confirm-email'),
    path('password-reset', ResetPasswordView.as_view(), name='reset-password'),
]