import pyotp

from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

import mayan
from mayan.apps.authentication.forms import AuthenticationFormBase
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
        #username_password_form_index = '0'

        #form_class = wizard.form_list[username_password_form_index]
        #cleaned_data = wizard.get_cleaned_data_for_step(username_password_form_index)

        user_id = wizard.request.session.get('_multi_factor_user_id', None)

        if user_id:
            user = get_user_model().objects.get(pk=user_id)
            #breakpoint()
            print("@@@@ FIELD", authentication_backend.form_class.PASSWORD_FIELD)
            kwargs = {
                #'user__{}'.format(form_class.PASSWORD_FIELD): cleaned_data['username']
                'user__{}'.format(authentication_backend.form_class.PASSWORD_FIELD): user.username
            }

            try:
                otp_data = UserOTPData.objects.get(**kwargs)
                    # ~ user__username=cleaned_data['username']
                # ~ )
            except UserOTPData.DoesNotExist:
                ###FIX This path should not exist.
                print("!!!!! False")
                return False
            else:
                print("otp_data.is_enabled", otp_data.is_enabled())
                return otp_data.is_enabled()
        else:
            return False

    # ~ def clean(self):
        # ~ form = self.wizard.get_form('0')
        # ~ form.cleaned_data = self.wizard.get_cleaned_data_for_step('0')
        # ~ form.clean()

        # ~ otp_data = form.get_user().otp_data


        # ~ secret = otp_data.secret

        # ~ token = self.cleaned_data.get('token')

        # ~ if token != pyotp.TOTP(secret).now():
            # ~ raise forms.ValidationError(
                # ~ self.error_messages['invalid_token'],
                # ~ code='invalid_token',
            # ~ )

        # ~ return self.cleaned_data

    def clean(self):
        # ~ form = self.wizard.get_form('0')
        # ~ form.cleaned_data = self.wizard.get_cleaned_data_for_step('0')
        # ~ form.clean()

        #user = form.get_user()

        #user_id = self.wizard.request.get('_multi_factor_user_id', None)
        user_id = self.request.session.get('_multi_factor_user_id', None)

        #if user:
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
