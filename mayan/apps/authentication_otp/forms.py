import pyotp

from django import forms
from django.utils.translation import ugettext_lazy as _

from mayan.apps.authentication.forms import AuthenticationFormBase

USER_SECRETS = {
    1: 'E6RSDCL732JFO3RZZN57CUPEOOCOJCUT'
}


class AuthenticationFormTOTP(AuthenticationFormBase):
    token = forms.CharField(
        label=_('TOTP token'), widget=forms.TextInput(
            attrs={'autofocus': True}
        )
    )
    error_messages = {
        'invalid_token': _(
            'Token is either invalid or expired.'
        ),
    }

    def clean(self):
        form = self.wizard.get_form('0')
        form.cleaned_data = self.wizard.get_cleaned_data_for_step('0')
        form.clean()

        secret = USER_SECRETS[form.get_user().pk]

        token = self.cleaned_data.get('token')

        if token != pyotp.TOTP(secret).now():
            raise forms.ValidationError(
                self.error_messages['invalid_token'],
                code='invalid_token',
            )

        return self.cleaned_data
