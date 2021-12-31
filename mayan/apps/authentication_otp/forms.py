import pyotp

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

import mayan
from mayan.apps.authentication.forms import AuthenticationFormBase
from mayan.apps.converter.fields import QRCodeImageField
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
    qr_code = QRCodeImageField(
        disabled=True, label=_('QR code'), required=False
    )
    secret = forms.CharField(
        disabled=True, label=_('Secret'), required=False,
        widget=forms.TextInput(
            attrs={'readonly': 'readonly'}
        )
    )
    signed_secret = forms.CharField(
        label=_('Secret'), required=False, widget=forms.HiddenInput(
            attrs={'readonly': 'readonly'}
        )
    )
    token = forms.CharField(label=_('Token'))

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')

        super().__init__(*args, **kwargs)

        secret = self.initial['secret']
        if secret:
            topt = pyotp.totp.TOTP(s=secret)
            url = topt.provisioning_uri(
                name=user.email, issuer_name=mayan.__title__
            )

            self.fields['qr_code'].initial = url

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
