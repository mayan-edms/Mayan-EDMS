import warnings

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.forms.widgets import EmailInput
from django.utils.translation import ugettext_lazy as _

from mayan.apps.user_management.querysets import get_user_queryset
from mayan.apps.views.forms import FilteredSelectionForm

from .permissions import permission_users_impersonate


class AuthenticationFormBase(forms.Form):
    _label = None

    def done(cls, wizard):
        return


class AuthenticationFormMixinRememberMe(forms.Form):
    _form_field_name_remember_me = 'remember_me'
    remember_me = forms.BooleanField(label=_('Remember me'), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        field_order = [
            field for field in self.fields if field != self._form_field_name_remember_me
        ]
        field_order.append(self._form_field_name_remember_me)

        self.order_fields(field_order=field_order)


class AuthenticationFormTOTP(AuthenticationFormBase):
    token = UsernameField(
        label=_('TOTP token'), widget=forms.TextInput(
            attrs={'autofocus': True}
        )
    )


class AuthenticationFormUsernamePassword(
    AuthenticationFormMixinRememberMe, AuthenticationForm,
    AuthenticationFormBase
):
    username = UsernameField(
        label=_('Username'), widget=forms.TextInput(
            attrs={'autofocus': True}
        )
    )
    password = forms.CharField(
        label=_('Password'), strip=False, widget=forms.PasswordInput
    )


class AuthenticationFormEmail(forms.Form):
    """
    A form to use email address authentication
    """
    email = forms.CharField(
        label=_('Email'), max_length=254, widget=EmailInput()
    )
    password = forms.CharField(
        label=_('Password'), widget=forms.PasswordInput
    )
    remember_me = forms.BooleanField(label=_('Remember me'), required=False)

    error_messages = {
        'invalid_login': _('Please enter a correct email and password. '
                           'Note that the password field is case-sensitive.'),
        'inactive': _('This account is inactive.'),
    }

    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def _authenticate(self, email=None, password=None):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=email)
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a non-existing user (#20760).
            UserModel().set_password(password)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = self._authenticate(email=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                )
            elif not self.user_cache.is_active:
                raise forms.ValidationError(
                    self.error_messages['inactive'],
                    code='inactive',
                )
        return self.cleaned_data

    def check_for_test_cookie(self):
        warnings.warn(
            'check_for_test_cookie is deprecated; ensure your login '
            'view is CSRF-protected.', DeprecationWarning
        )

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache


class UserImpersonationOptionsForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['permanent'] = forms.BooleanField(
            label=_('Permanent'), help_text=_(
                'If selected, disables ending impersonation.'
            ), required=False
        )


class UserImpersonationSelectionForm(
    FilteredSelectionForm, UserImpersonationOptionsForm
):
    class Meta:
        allow_multiple = False
        field_name = 'user_to_impersonate'
        label = _('User')
        queryset = get_user_queryset().none()
        permission = permission_users_impersonate
        required = True
        widget_attributes = {'class': 'select2'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        queryset = get_user_queryset().exclude(pk=kwargs['user'].pk)
        self.fields['user_to_impersonate'].queryset = queryset
        self.order_fields(field_order=('user_to_impersonate', 'permanent'))


class UsernameAuthenticationForm(AuthenticationForm):
    remember_me = forms.BooleanField(label=_('Remember me'), required=False)
