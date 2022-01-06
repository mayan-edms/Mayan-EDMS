from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _

from mayan.apps.user_management.querysets import get_user_queryset
from mayan.apps.views.forms import FilteredSelectionForm

from .permissions import permission_users_impersonate


class AuthenticationFormBase(forms.Form):
    _label = None
    PASSWORD_FIELD = 'username'

    def __init__(self, data, files, prefix, initial, request=None, wizard=None):
        self.request = request
        self.user_cache = None
        self.wizard = wizard

        super().__init__(
            data=data, files=files, prefix=prefix, initial=initial
        )

    def get_user(self):
        return self.user_cache


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


class AuthenticationFormEmailPassword(
    AuthenticationFormMixinRememberMe, AuthenticationForm
):
    """
    A form to use email address authentication.
    """
    PASSWORD_FIELD = 'email'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        UserModel = get_user_model()

        self.username_field = UserModel._meta.get_field(field_name='email')
        username_max_length = self.username_field.max_length or 254
        self.fields['username'].max_length = username_max_length
        self.fields['username'].widget.attrs['maxlength'] = username_max_length
        self.fields['username'].label = self.username_field.verbose_name


class AuthenticationFormUsernamePassword(
    AuthenticationFormMixinRememberMe, AuthenticationForm
):
    """
    Modified authentication form to include the "Remember me" field.
    """
    PASSWORD_FIELD = 'username'


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
