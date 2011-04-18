from django import forms
from django.utils.translation import ugettext as _
#from django.template.defaultfilters import capfirst

from models import Folder


class FolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ('title',)
