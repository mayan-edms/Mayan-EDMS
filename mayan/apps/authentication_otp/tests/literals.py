TEST_AUTHENTICATION_BACKEND_USERNAME_OTP = 'mayan.apps.authentication_otp.authentication_backends.AuthenticationBackendModelUsernamePasswordTOTP'
TEST_PASSWORD_NEW = 'new_password_123'


from mayan.apps.common.utils import get_class_full_name

from ..authentication_backends import (
    AuthenticationBackendModelEmailPasswordTOTP,
    AuthenticationBackendModelUsernamePasswordTOTP
)

PATH_AUTHENTICATION_BACKEND_EMAIL_OTP = get_class_full_name(
    klass=AuthenticationBackendModelEmailPasswordTOTP
)
PATH_AUTHENTICATION_BACKEND_USERNAME_OTP = get_class_full_name(
    klass=AuthenticationBackendModelUsernamePasswordTOTP
)
