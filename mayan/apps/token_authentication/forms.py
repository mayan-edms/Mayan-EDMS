from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _


class TokenAuthenticationForm(AuthenticationForm):
    remember_me = forms.BooleanField(label=_('Remember me'), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
