from mayan.apps.authentication.authentication_backends import AuthenticationBackendModelUsernamePassword

from .forms import AuthenticationFormTOTP


class AuthenticationBackendOTPMixin:
    def __init__(self, **kwargs):
        self.form_list += (AuthenticationFormTOTP,)
        super().__init__(**kwargs)


class AuthenticationBackendModelUsernamePasswordOTP(
    AuthenticationBackendOTPMixin, AuthenticationBackendModelUsernamePassword
):
    """
    Same backend as AuthenticationBackendModelUsernamePassword but with
    an additional form for and TOTP token.
    """
