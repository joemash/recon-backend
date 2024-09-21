from django_rest_passwordreset.views import (
    ResetPasswordConfirmViewSet,
    ResetPasswordRequestTokenViewSet,
)
from rest_framework.routers import DefaultRouter

from src.account.views.change_password import ChangePasswordViewSet
from src.account.views.login import LoginViewSet
from src.account.views.register import RegisterUserViewSet


user_router = DefaultRouter()
user_router.register(r"register", RegisterUserViewSet, basename="register")
user_router.register(r"login", LoginViewSet, basename="login")
user_router.register(
    r"change-password", ChangePasswordViewSet, basename="change-password"
)

password_router = DefaultRouter()
password_router.register(
    r"forgot_password", ResetPasswordRequestTokenViewSet, basename="forgot_password"
)
password_router.register(
    r"confirm_password", ResetPasswordConfirmViewSet, basename="reset_password"
)
