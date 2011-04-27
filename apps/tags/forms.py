from django import forms
from django.utils.translation import ugettext as _

from taggit.models import Tag


#class FolderForm(forms.ModelForm):
#    class Meta:
#        model = Folder
#        fields = ('title',)


class AddTagForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        #user = kwargs.pop('user', None)
        super(AddTagForm, self).__init__(*args, **kwargs)
        #self.fields['title'].required = False
        #self.fields['title'].label = _(u'New folder')

        self.fields['existing_tags'] = forms.ModelChoiceField(
            required=False,
            queryset=Tag.objects.all(),  #(user=user),
            label=_(u'Existing tags'))
        self.fields['name'].required = False
        self.fields['name'].label = _(u'New tag')

    class Meta:
        model = Tag
        fields = ('name',)
