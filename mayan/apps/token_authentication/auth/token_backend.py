from django.apps import apps
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class TokenBackend(ModelBackend):
    def authenticate(self, request, token=None):
        UserModel = get_user_model()
        Token = apps.get_model('authtoken', 'Token')

        try:
            token = Token.objects.select_related('user').get(key=token)
        except Token.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a non-existing user (#20760).
            UserModel().set_password(token or '')
        else:
            return token.user
