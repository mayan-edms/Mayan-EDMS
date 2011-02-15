from django import forms
from django.utils.translation import ugettext_lazy as _

from common.forms import DetailForm

from models import Role


class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
    

class RoleForm_view(DetailForm):
    class Meta:
        model = Role
        
