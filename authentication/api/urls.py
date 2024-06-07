from django.urls import path

from .views.main.create_user import CreateUserView
from .views.main.login_user import LoginUser
from .views.main.update_user import UpdateUser
from .views.main.logout import Logout
from .views.main.deactivate_account import DeactivateAccount
from .views.checkers.check_user_authenticated import CheckUserAuthenticated
from .views.checkers.check_user_confirmed import CheckUserConfirmed
from .views.checkers.confirm_email import ConfirmEmailAddress
from .views.main.reset_password.change_password import ChangePassword
from .views.others.resend_confirmation_email import ResendConfirmationEmail
from .views.others.renew_access_token import RenewAccessToken
from .views.main.reset_password.reset_password import ResetUserPassword
from .views.checkers.check_reset_link_confirmed import CheckResetLinkConfirmed
from .views.others.change_user_password import ChangeUserPassword
from rest_framework import routers

urlpatterns = [
    path("create/", CreateUserView.as_view(), name="create_user"),
    path("login/", LoginUser.as_view(), name="login_user"),
    path(
        "checkuserauthenticated/",
        CheckUserAuthenticated.as_view(),
        name="check_user_authenticated",
    ),
    path("update/", UpdateUser.as_view(), name="update_user"),
    path(
        "confirm-email/<str:token>/",
        ConfirmEmailAddress.as_view(),
        name="confirm_email",
    ),
    path(
        "reset-confirmation/",
        CheckResetLinkConfirmed.as_view(),
        name="reset_password_confirm",
    ),
    path(
        "resend-confirmation/",
        ResendConfirmationEmail.as_view(),
        name="resend-confirmation",
    ),
    path("change-password/", ChangePassword.as_view(), name="reset_password"),
    path("logout/", Logout.as_view(), name="logout_user"),
    path("deactivate/", DeactivateAccount.as_view(), name="deactivate"),
    path("confirmed/", CheckUserConfirmed.as_view(), name="check-confirmed"),
    path("renew-access-token/", RenewAccessToken.as_view(), name="renew-access-token"),
    path("reset-password/", ResetUserPassword.as_view(), name="reset-password"),
    path(
        "auth-change-user-password/",
        ChangeUserPassword.as_view(),
        name="auth-change-user-password",
    ),
]

# router = routers.SimpleRouter()
