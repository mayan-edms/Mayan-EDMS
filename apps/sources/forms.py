from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext

from documents.forms import DocumentForm

from sources.models import WebForm, StagingFolder, SourceTransformation, \
    WatchFolder
from sources.widgets import FamFamRadioSelect
from sources.utils import validate_whitelist_blacklist


class StagingDocumentForm(DocumentForm):
    """
    Form that show all the files in the staging folder specified by the
    StagingFile class passed as 'cls' argument
    """
    def __init__(self, *args, **kwargs):
        cls = kwargs.pop('cls')
        show_expand = kwargs.pop('show_expand', False)
        self.source = kwargs.pop('source')
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
        self.source = kwargs.pop('source')
        super(WebFormForm, self).__init__(*args, **kwargs)
        print self.instance

        if show_expand:
            self.fields['expand'] = forms.BooleanField(
                label=_(u'Expand compressed files'), required=False,
                help_text=ugettext(u'Upload a compressed file\'s contained files as individual documents')
            )

    def clean_file(self):
        data = self.cleaned_data['file']
        validate_whitelist_blacklist(data.name, self.source.whitelist.split(','), self.source.blacklist.split(','))

        return data


class WebFormSetupForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(WebFormSetupForm, self).__init__(*args, **kwargs)
        self.fields['icon'].widget = FamFamRadioSelect(
            attrs=self.fields['icon'].widget.attrs,
            choices=self.fields['icon'].widget.choices,
        )

    class Meta:
        model = WebForm


class StagingFolderSetupForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(StagingFolderSetupForm, self).__init__(*args, **kwargs)
        self.fields['icon'].widget = FamFamRadioSelect(
            attrs=self.fields['icon'].widget.attrs,
            choices=self.fields['icon'].widget.choices,
        )

    class Meta:
        model = StagingFolder


class WatchFolderSetupForm(forms.ModelForm):
    class Meta:
        model = WatchFolder


class SourceTransformationForm(forms.ModelForm):
    class Meta:
        model = SourceTransformation

    def __init__(self, *args, **kwargs):
        super(SourceTransformationForm, self).__init__(*args, **kwargs)
        self.fields['content_type'].widget = forms.HiddenInput()
        self.fields['object_id'].widget = forms.HiddenInput()


class SourceTransformationForm_create(forms.ModelForm):
    class Meta:
        model = SourceTransformation
        exclude = ('content_type', 'object_id')
