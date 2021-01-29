import warnings

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import EmailInput
from django.utils.translation import ugettext_lazy as _

from mayan.apps.user_management.querysets import get_user_queryset
from mayan.apps.views.forms import FilteredSelectionForm

from .permissions import permission_users_impersonate


class EmailAuthenticationForm(forms.Form):
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

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(email=email, password=password)
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
