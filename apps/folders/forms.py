from django import forms
from django.utils.translation import ugettext_lazy as _

from folders.models import Folder


class FolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ('title',)


class AddDocumentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(AddDocumentForm, self).__init__(*args, **kwargs)
        self.fields['existing_folder'] = forms.ModelChoiceField(
            required=False,
            queryset=Folder.objects.filter(user=user),
            label=_(u'Existing folders'))
        self.fields['title'].required = False
        self.fields['title'].label = _(u'New folder')

    class Meta:
        model = Folder
        fields = ('title',)
