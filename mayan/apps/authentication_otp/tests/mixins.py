import pyotp


class AuthenticationOTPTestMixin:
    def _enable_test_otp(self):
        self._test_secret = pyotp.random_base32()
        self._test_totp = pyotp.TOTP(self._test_secret)

        self._test_token = self._test_totp.now()
        self._test_case_superuser.otp_data.enable(
            secret=self._test_secret, token=self._test_token
        )
