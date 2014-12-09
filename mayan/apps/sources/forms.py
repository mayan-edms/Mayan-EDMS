from __future__ import absolute_import

import logging

from django import forms
from django.utils.translation import ugettext
from django.utils.translation import ugettext_lazy as _

from documents.forms import DocumentForm
from documents.models import DocumentVersion

from .models import (IMAPEmail, POP3Email, SourceTransformation,
                     StagingFolderSource, WebFormSource, WatchFolderSource)

logger = logging.getLogger(__name__)


class NewDocumentForm(DocumentForm):
    class Meta(DocumentForm.Meta):
        exclude = ('label',)


class NewVersionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        document = kwargs.pop('document')
        super(NewVersionForm, self).__init__(*args, **kwargs)

        self.fields['comment'] = forms.CharField(
            label=_(u'Comment'),
            required=False,
            widget=forms.widgets.Textarea(attrs={'rows': 4}),
        )


class UploadBaseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        show_expand = kwargs.pop('show_expand', False)
        self.source = kwargs.pop('source')

        super(UploadBaseForm, self).__init__(*args, **kwargs)

        if show_expand:
            self.fields['expand'] = forms.BooleanField(
                label=_(u'Expand compressed files'), required=False,
                help_text=ugettext(u'Upload a compressed file\'s contained files as individual documents')
            )


class StagingUploadForm(UploadBaseForm):
    """
    Form that show all the files in the staging folder specified by the
    StagingFile class passed as 'cls' argument
    """
    def __init__(self, *args, **kwargs):
        super(StagingUploadForm, self).__init__(*args, **kwargs)

        try:
            self.fields['staging_file_id'].choices = [
                (staging_file.encoded_filename, unicode(staging_file)) for staging_file in self.source.get_files()
            ]
        except Exception as exception:
            logger.error('exception: %s', exception)
            pass

        # Put staging_list field first in the field order list
        staging_list_index = self.fields.keyOrder.index('staging_file_id')
        staging_list = self.fields.keyOrder.pop(staging_list_index)
        self.fields.keyOrder.insert(0, staging_list)

    staging_file_id = forms.ChoiceField(label=_(u'Staging file'))


class WebFormUploadForm(UploadBaseForm):
    file = forms.FileField(label=_(u'File'))

    def __init__(self, *args, **kwargs):
        super(WebFormUploadForm, self).__init__(*args, **kwargs)

        # Move the file filed to the top
        self.fields.keyOrder.remove('file')
        self.fields.keyOrder.insert(0, 'file')


class WebFormSetupForm(forms.ModelForm):
    class Meta:
        model = WebFormSource


class StagingFolderSetupForm(forms.ModelForm):
    class Meta:
        model = StagingFolderSource


class POP3EmailSetupForm(forms.ModelForm):
    class Meta:
        model = POP3Email


class IMAPEmailSetupForm(forms.ModelForm):
    class Meta:
        model = IMAPEmail


class WatchFolderSetupForm(forms.ModelForm):
    class Meta:
        model = WatchFolderSource


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
