from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

from mayan.apps.databases.classes import BaseBackend


class DjangoAuthenticationBackendModelEmail(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()

        if username is None or password is None:
            return
        try:
            user = UserModel._default_manager.get(email=username)
        except UserModel.DoesNotExist:
            # Execute the default password hasher to avoid valid user
            # discovery via differential timming analysis.
            UserModel().set_password(raw_password=password)
        else:
            if user.check_password(raw_password=password) and self.user_can_authenticate(user=user):
                return user


class DjangoAuthenticationBackendWrapperMultiFactor(BaseBackend):
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
        factor_instance = factor['class']()

        return factor_instance.authenticate(request, **kwargs)

    def get_user(self, user_id, **kwargs):
        factor_name = kwargs.pop('factor_name', None)

        factor = self._get_factor(factor_name=factor_name)
        factor_instance = factor['class']()

        return factor_instance.get_user(user_id=user_id)
