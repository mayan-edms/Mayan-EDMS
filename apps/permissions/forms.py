from django import forms
from django.utils.translation import ugettext_lazy as _
#from django.http import HttpResponseRedirect
#from django.utils.http import urlencode
#from django.core.urlresolvers import reverse
#from django.utils.safestring import mark_safe
#from django.forms.formsets import formset_factory

#from common.wizard import BoundFormWizard
#from common.utils import urlquote
from common.forms import DetailForm

from models import Role


class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
    

class RoleForm_view(DetailForm):
    class Meta:
        model = Role
        
