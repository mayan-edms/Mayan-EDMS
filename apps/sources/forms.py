from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext

from documents.forms import DocumentForm

from sources.models import WebForm, StagingFolder


class StagingDocumentForm(DocumentForm):
    """
    Form that show all the files in the staging folder specified by the
    StagingFile class passed as 'cls' argument
    """
    def __init__(self, *args, **kwargs):
        cls = kwargs.pop('cls')
        show_expand = kwargs.pop('show_expand', False)
        super(StagingDocumentForm, self).__init__(*args, **kwargs)
        try:
            self.fields['staging_file_id'].choices = [
                (staging_file.id, staging_file) for staging_file in cls.get_all()
            ]
        except:
            pass

        if show_expand:
            self.fields['expand'] = forms.BooleanField(
                label=_(u'Expand compressed files'), required=False,
                help_text=ugettext(u'Upload a compressed file\'s contained files as individual documents')
            )

        # Put staging_list field first in the field order list
        staging_list_index = self.fields.keyOrder.index('staging_file_id')
        staging_list = self.fields.keyOrder.pop(staging_list_index)
        self.fields.keyOrder.insert(0, staging_list)

    staging_file_id = forms.ChoiceField(label=_(u'Staging file'))

    class Meta(DocumentForm.Meta):
        exclude = ('description', 'file', 'document_type', 'tags')


class WebFormForm(DocumentForm):
    def __init__(self, *args, **kwargs):
        show_expand = kwargs.pop('show_expand', False)
        super(WebFormForm, self).__init__(*args, **kwargs)

        if show_expand:
            self.fields['expand'] = forms.BooleanField(
                label=_(u'Expand compressed files'), required=False,
                help_text=ugettext(u'Upload a compressed file\'s contained files as individual documents')
            )


class WebFormSetupForm(forms.ModelForm):
    class Meta:
        model = WebForm
        
        
class StagingFolderSetupForm(forms.ModelForm):
    class Meta:
        model = StagingFolder
