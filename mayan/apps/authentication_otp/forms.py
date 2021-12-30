import pyotp

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from mayan.apps.authentication.forms import AuthenticationFormBase
from mayan.apps.views.forms import DetailForm

from .models import UserOTPData


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

    @classmethod
    def condition(cls, wizard):
        cleaned_data = wizard.get_cleaned_data_for_step('0')
        if cleaned_data:
            otp_data = UserOTPData.objects.get(
                user__username=cleaned_data['username']
            )

            return otp_data.is_enabled()
        else:
            return False

    def clean(self):
        form = self.wizard.get_form('0')
        form.cleaned_data = self.wizard.get_cleaned_data_for_step('0')
        form.clean()

        otp_data = form.get_user().otp_data

        secret = otp_data.secret

        token = self.cleaned_data.get('token')

        if token != pyotp.TOTP(secret).now():
            raise forms.ValidationError(
                self.error_messages['invalid_token'],
                code='invalid_token',
            )

        return self.cleaned_data


class FormUserOTPDataDetail(DetailForm):
    def __init__(self, *args, **kwargs):
        instance = kwargs['instance']
        extra_fields = ()

        otp_enabled = instance.otp_data.is_enabled()

        extra_fields = (
            {
                'label': _('OTP enabled?'),
                'func': lambda instance: _('Yes') if otp_enabled else _('No')
            },
        )

        kwargs['extra_fields'] = extra_fields
        super().__init__(*args, **kwargs)

    class Meta:
        fields = ()
        model = UserOTPData


class FormUserOTPDataEdit(forms.Form):
    secret = forms.CharField(
        required=False, widget=forms.TextInput(
            attrs={'readonly': 'readonly'}
        )
    )
    token = forms.CharField()

    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial', {})
        initial['secret'] = initial.get('initial', pyotp.random_base32())
        kwargs.update({'initial': initial})

        super().__init__(*args, **kwargs)

    def clean_token(self):
        secret = self.cleaned_data['secret']
        token = self.cleaned_data['token']

        totp = pyotp.TOTP(secret)

        if token.strip() != totp.now():
            raise ValidationError(
                _('Token is incorrect for the specified secret.'),
                code='token_invalid'
            )

        return token
