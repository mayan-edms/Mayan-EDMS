import pyotp

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


class UserOTPData(models.Model):
    """
    This model stores OTP configurations for a user account.
    """
    user = models.OneToOneField(
        on_delete=models.CASCADE, related_name='otp_data',
        to=settings.AUTH_USER_MODEL, unique=True, verbose_name=_('User')
    )
    secret = models.CharField(
        blank=True, max_length=96, verbose_name=_(
            '16 character, base32 encoded random string.'
        )
    )

    class Meta:
        verbose_name = _('User OTP data')
        verbose_name_plural = _('Users OTP data')

    def disable(self):
        self.secret = ''
        self.save()

    def enable(self, secret, token):
        totp = pyotp.TOTP(s=secret)

        if token == totp.now():
            self.secret = secret
            self.save()

    def get_absolute_url(self):
        return reverse(viewname='authentication_otp:otp_detail')

    def is_enabled(self):
        if self.secret:
            return True
        else:
            return False

    def natural_key(self):
        return self.user.natural_key()
    natural_key.dependencies = [settings.AUTH_USER_MODEL]
