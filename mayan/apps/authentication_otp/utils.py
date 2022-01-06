from mayan.apps.authentication.settings import setting_authentication_backend
from mayan.apps.common.utils import get_class_full_name


def is_otp_backend_enabled():
    # Hide import.
    from .authentication_backends import AuthenticationBackendModelUsernamePasswordTOTP

    return setting_authentication_backend.value == get_class_full_name(
        klass=AuthenticationBackendModelUsernamePasswordTOTP
    )
