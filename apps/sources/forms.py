from __future__ import absolute_import

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext

from documents.forms import DocumentForm

from .models import (WebForm, StagingFolder, SourceTransformation,
    WatchFolder, POP3Email, IMAPEmail, LocalScanner)
from .widgets import IconRadioSelect
from .utils import validate_whitelist_blacklist


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
    file = forms.FileField(label=_(u'File'))

    def __init__(self, *args, **kwargs):
        show_expand = kwargs.pop('show_expand', False)
        self.source = kwargs.pop('source')
        super(WebFormForm, self).__init__(*args, **kwargs)

        if show_expand:
            self.fields['expand'] = forms.BooleanField(
                label=_(u'Expand compressed files'), required=False,
                help_text=ugettext(u'Upload a compressed file\'s contained files as individual documents')
            )

        # Move the file filed to the top
        self.fields.keyOrder.remove('file')
        self.fields.keyOrder.insert(0, 'file')

    def clean_file(self):
        data = self.cleaned_data['file']
        validate_whitelist_blacklist(data.name, self.source.whitelist.split(','), self.source.blacklist.split(','))

        return data


class WebFormSetupForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(WebFormSetupForm, self).__init__(*args, **kwargs)
        self.fields['icon'].widget = IconRadioSelect(
            attrs=self.fields['icon'].widget.attrs,
            choices=self.fields['icon'].widget.choices,
        )

    class Meta:
        model = WebForm


class StagingFolderSetupForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(StagingFolderSetupForm, self).__init__(*args, **kwargs)
        self.fields['icon'].widget = IconRadioSelect(
            attrs=self.fields['icon'].widget.attrs,
            choices=self.fields['icon'].widget.choices,
        )

    class Meta:
        model = StagingFolder


class WatchFolderSetupForm(forms.ModelForm):
    class Meta:
        model = WatchFolder


class LocalScannerSetupForm(forms.ModelForm):
    class Meta:
        model = LocalScanner

    scanner = forms.ChoiceField(required=False, label=_(u'Active scanners'), help_text=_(u'List of scanners found connected to this node.  Choose one to have its device and description automatically saved in the fields above.'))
    scanner_device = forms.CharField(required=False, label=_(u'Scanner device'))
    scanner_description = forms.CharField(required=False, label=_(u'Scanner description'))
            
    def __init__(self, *args, **kwargs):
        super(LocalScannerSetupForm, self).__init__(*args, **kwargs)
        self.fields['icon'].widget = IconRadioSelect(
            attrs=self.fields['icon'].widget.attrs,
            choices=self.fields['icon'].widget.choices,
        )
        self.scanner_choices = LocalScanner.get_scanner_choices()
        self.fields['scanner'].choices = self.scanner_choices

    def clean(self):
        try:
            scanner = LocalScanner.get_scanner(self.cleaned_data.get('scanner'))
        except LocalScanner.NoSuchScanner:
            device_name = u''
            description = u''
        else:
            device_name = scanner['scanner']._device
            description = scanner['description']
            
        self.cleaned_data['scanner_device'] = device_name
        self.cleaned_data['scanner_description'] = description
        return self.cleaned_data


class LocalScannerForm(DocumentForm):
    def __init__(self, *args, **kwargs):
        show_expand = kwargs.pop('show_expand', False)
        self.source = kwargs.pop('source')
        super(LocalScannerForm, self).__init__(*args, **kwargs)
        self.fields['new_filename'].help_text=_(u'If left blank a date time stamp will be used.')

    def clean_file(self):
        data = self.cleaned_data['file']
        validate_whitelist_blacklist(data.name, self.source.whitelist.split(','), self.source.blacklist.split(','))

        return data
        

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


class EmailSetupForm(forms.ModelForm):
    class Meta:
        widgets = {
            'password': forms.widgets.PasswordInput,
        }


class POP3EmailSetupForm(EmailSetupForm):
    class Meta(EmailSetupForm.Meta):
        model = POP3Email


class IMAPEmailSetupForm(EmailSetupForm):
    class Meta(EmailSetupForm.Meta):
        model = IMAPEmail
