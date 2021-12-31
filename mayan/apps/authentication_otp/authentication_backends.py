from mayan.apps.authentication.authentication_backends import (
    AuthenticationBackendModelEmailPassword,
    AuthenticationBackendModelUsernamePassword
)

from .forms import AuthenticationFormTOTP


class AuthenticationBackendTOTPMixin:
    def __init__(self, **kwargs):
        self.form_list += (AuthenticationFormTOTP,)
        super().__init__(**kwargs)


class AuthenticationBackendModelEmailPasswordTOTP(
    AuthenticationBackendTOTPMixin, AuthenticationBackendModelEmailPassword
):
    """
    Same backend as AuthenticationBackendModelEmailPassword but with
    an additional form for an TOTP token.
    """


class AuthenticationBackendModelUsernamePasswordTOTP(
    AuthenticationBackendTOTPMixin,
    AuthenticationBackendModelUsernamePassword
):
    """
    Same backend as AuthenticationBackendModelUsernamePassword but with
    an additional form for an TOTP token.
    """
