from django.contrib.auth.backends import BaseBackend, ModelBackend

from mayan.apps.authentication.django_authentication_backends import (
    DjangoAuthenticationBackendModelEmail,
    DjangoAuthenticationBackendWrapperMultiFactor
)


class DjangoAuthenticationBackendOTP(BaseBackend):
    def authenticate(self, request, otp_token, user):
        if user:
            if user.otp_data.is_enabled():
                if user.otp_data.verify_token(token=otp_token):
                    return user
                else:
                    return
            else:
                return user
        else:
            return


class DjangoAuthenticationBackendEmailMultiFactorOTP(
    DjangoAuthenticationBackendWrapperMultiFactor
):
    factors = (
        {
            'default': True,
            'class': DjangoAuthenticationBackendModelEmail,
            'name': 'email_password'
        },
        {
            'class': DjangoAuthenticationBackendOTP,
            'name': 'otp_token'
        }
    )


class DjangoAuthenticationBackendUsernameMultiFactorOTP(
    DjangoAuthenticationBackendWrapperMultiFactor
):
    factors = (
        {
            'default': True,
            'class': ModelBackend,
            'name': 'username_password'
        },
        {
            'class': DjangoAuthenticationBackendOTP,
            'name': 'otp_token'
        }
    )
