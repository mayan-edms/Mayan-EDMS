from django.conf import settings
from django.contrib.auth.backends import BaseBackend, ModelBackend

from mayan.apps.authentication.authentication_backends import (
    AuthenticationBackendModelEmailPassword,
    AuthenticationBackendModelUsernamePassword, EmailModelBackend
)
from mayan.apps.common.utils import get_class_full_name

from .forms import AuthenticationFormTOTP


class AuthenticationBackendTOTPMixin:
    def __init__(self, **kwargs):
        #self.form_list[0].clean = lambda self: return self.cleaned_data
        self.form_list += (AuthenticationFormTOTP,)

        super().__init__(**kwargs)



class DjangoAuthenticationBackendMultiFactor(BaseBackend):
    #_factor_cache = {}

    factors = ()
    _default_factor = None
    _factor_instance = None
    _factors_map = {}

    def _get_factor(self, factor_name=None):
        if not factor_name:
            return self._default_factor
        else:
            return self._factors_map[factor_name]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for factor_entry in self.factors:
            factor_name = factor_entry['name']
            if factor_entry.get('default', False):
                self._default_factor = factor_entry

            self._factors_map[factor_name] = factor_entry

    def authenticate(self, request, **kwargs):
        factor_name = kwargs.pop('factor_name', None)

        factor = self._get_factor(factor_name=factor_name)
        #self.__class__._factor_instance = factor['class']()
        factor_instance = factor['class']()

        #return self._factor_instance.authenticate(request, **kwargs)
        return factor_instance.authenticate(request, **kwargs)

    def get_user(self, user_id, **kwargs):
        factor_name = kwargs.pop('factor_name', None)

        factor = self._get_factor(factor_name=factor_name)
        #self.__class__._factor_instance = factor['class']()
        factor_instance = factor['class']()

        #return self._factor_instance.get_user(request, **kwargs)
        return factor_instance.get_user(user_id=user_id)


        # ~ if self.__class__._factor_instance:
            # ~ return self.__class__._factor_instance.get_user(user_id=user_id)


class DjangoAuthenticationBackendOTP(BaseBackend):
    def authenticate(self, request, otp_token, user):
        otp_data = user.otp_data
        secret = otp_data.secret

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


class DjangoAuthenticationBackendMultiFactorOTP(
    DjangoAuthenticationBackendMultiFactor
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




# ~ class ModelBackendUsernameOTP(ModelBackend):
    # ~ def authenticate(self, request, token=None, username=None, password=None, **kwargs):
        # ~ user = super().authenticate(request=request, username=username, password=password, **kwargs)

        # ~ if user:
            # ~ if user.otp_data.is_enabled():
                # ~ if user.otp_data.verify_token(token=token):
                    # ~ return user
                # ~ else:
                    # ~ return
            # ~ else:
                # ~ return user
        # ~ else:
            # ~ return


class AuthenticationBackendModelEmailPasswordTOTP(
    AuthenticationBackendTOTPMixin, AuthenticationBackendModelEmailPassword
):
    """
    Same backend as AuthenticationBackendModelEmailPassword but with
    an additional form for an TOTP token.
    """
    def initialize(self):
        settings.AUTHENTICATION_BACKENDS = (
            get_class_full_name(klass=DjangoAuthenticationBackendMultiFactorOTP),
        )


class AuthenticationBackendModelUsernamePasswordTOTP(
    AuthenticationBackendTOTPMixin,
    AuthenticationBackendModelUsernamePassword
):
    """
    Same backend as AuthenticationBackendModelUsernamePassword but with
    an additional form for an TOTP token.
    """
    # ~ def initialize(self):
        # ~ settings.AUTHENTICATION_BACKENDS = (
            # ~ get_class_full_name(klass=ModelBackendUsernameOTP),
        # ~ )
    def initialize(self):
        settings.AUTHENTICATION_BACKENDS = (
            get_class_full_name(klass=DjangoAuthenticationBackendMultiFactorOTP),
        )
