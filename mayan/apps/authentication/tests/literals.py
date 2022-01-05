from mayan.apps.common.utils import get_class_full_name

from ..authentication_backends import (
    AuthenticationBackendModelEmailPassword,
    AuthenticationBackendModelUsernamePassword
)

PATH_AUTHENTICATION_BACKEND_EMAIL = get_class_full_name(
    klass=AuthenticationBackendModelEmailPassword
)
PATH_AUTHENTICATION_BACKEND_USERNAME = get_class_full_name(
    klass=AuthenticationBackendModelUsernamePassword
)

TEST_PASSWORD_NEW = 'new_password_123'
