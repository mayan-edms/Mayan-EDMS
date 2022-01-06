import pyotp

from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

import mayan
from mayan.apps.authentication.forms import AuthenticationFormBase
from mayan.apps.authentication.literals import SESSION_MULTI_FACTOR_USER_ID_KEY
from mayan.apps.converter.fields import QRCodeImageField
from mayan.apps.views.forms import DetailForm

from .models import UserOTPData


class AuthenticationFormTOTP(AuthenticationFormBase):
    error_messages = {
        'invalid_token': _(
            'Token is either invalid or expired.'
        )
    }

    token = forms.CharField(
        label=_('TOTP token'), widget=forms.TextInput(
            attrs={
                'autocomplete': 'one-time-code', 'autofocus': True,
                'inputmode': 'numeric'
            }
        )
    )

    @classmethod
    def condition(cls, authentication_backend, wizard):
        user_id = wizard.request.session.get(
            SESSION_MULTI_FACTOR_USER_ID_KEY, None
        )

        if user_id:
            user = get_user_model().objects.get(pk=user_id)
            kwargs = {
                'user__{}'.format(
                    authentication_backend.login_form_class.PASSWORD_FIELD
                ): user.username
            }

            try:
                otp_data = UserOTPData.objects.get(**kwargs)
            except UserOTPData.DoesNotExist:
                return False
            else:
                return otp_data.is_enabled()
        else:
            return False

    def clean(self):
        user_id = self.request.session.get(SESSION_MULTI_FACTOR_USER_ID_KEY, None)

        if user_id:
            user = get_user_model().objects.get(pk=user_id)
            self.user_cache = authenticate(
                factor_name='otp_token',
                otp_token=self.cleaned_data.get('token'),
                request=self.request, user=user
            )
            if self.user_cache is None:
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
    qr_code = QRCodeImageField(disabled=True, label='', required=False)
    secret = forms.CharField(
        disabled=True,
        help_text=_(
            'Scan the QR code or enter the secret in your authentication '
            'device. Do not share this secret, treat it like a password.'
        ), label=_('Secret'), required=False, widget=forms.TextInput(
            attrs={'readonly': 'readonly'}
        )
    )
    signed_secret = forms.CharField(
        label=_('Secret'), required=False, widget=forms.HiddenInput(
            attrs={'readonly': 'readonly'}
        )
    )
    token = forms.CharField(
        help_text=_(
            'Enter the corresponding token to validate that the secret '
            'was saved correct.'
        ),
        label=_('Token'), widget=forms.TextInput(
            attrs={
                'autocomplete': 'one-time-code', 'autofocus': True,
                'inputmode': 'numeric'
            }
        )
    )

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

        self.fields['qr_code'].widget.attrs.update(
            {'style': 'margin:auto;'}
        )

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
