import logging
import os

from django import forms
from django.utils.translation import ugettext_lazy as _

from mayan.apps.views.forms import DetailForm

from ..models.document_models import Document
from ..settings import setting_language
from ..utils import get_language, get_language_choices

__all__ = ('DocumentForm', 'DocumentPropertiesForm',)
logger = logging.getLogger(name=__name__)


class DocumentForm(forms.ModelForm):
    """
    Base form for the minimal document properties. Meant to be subclassed.
    """
    class Meta:
        fields = ('label', 'description', 'language')
        model = Document

    def __init__(self, *args, **kwargs):
        document_type = kwargs.pop('document_type', None)

        super().__init__(*args, **kwargs)

        # Is a document (documents app edit) and has been saved (sources
        # app upload)?
        if self.instance and self.instance.pk:
            document_type = self.instance.document_type
        else:
            self.initial.update({'language': setting_language.value})

        filenames_queryset = document_type.filenames.filter(enabled=True)

        if filenames_queryset:
            self.fields[
                'document_type_available_filenames'
            ] = forms.ModelChoiceField(
                queryset=filenames_queryset,
                required=False,
                label=_('Quick document rename'),
                widget=forms.Select(
                    attrs={
                        'class': 'select2'
                    }
                )
            )
            self.fields['preserve_extension'] = forms.BooleanField(
                label=_('Preserve extension'), required=False,
                help_text=_(
                    'Takes the file extension and moves it to the end of the '
                    'filename allowing operating systems that rely on file '
                    'extensions to open document correctly.'
                )
            )

        self.fields['language'].widget = forms.Select(
            choices=get_language_choices(), attrs={
                'class': 'select2'
            }
        )

    def clean(self):
        self.cleaned_data['label'] = self.get_final_label(
            # Fallback to the instance label if there is no label key or
            # there is a label key and is an empty string
            filename=self.cleaned_data.get('label') or self.instance.label
        )

        return self.cleaned_data

    def get_final_label(self, filename):
        if 'document_type_available_filenames' in self.cleaned_data:
            if self.cleaned_data['document_type_available_filenames']:
                if self.cleaned_data['preserve_extension']:
                    filename, extension = os.path.splitext(filename)

                    filename = '{}{}'.format(
                        self.cleaned_data[
                            'document_type_available_filenames'
                        ].filename, extension
                    )
                else:
                    filename = self.cleaned_data[
                        'document_type_available_filenames'
                    ].filename

        return filename


class DocumentPropertiesForm(DetailForm):
    """
    Detail class form to display a document file based properties
    """
    def __init__(self, *args, **kwargs):
        document = kwargs['instance']

        extra_fields = [
            {
                'label': _('Date created'),
                'field': 'datetime_created',
                'widget': forms.widgets.DateTimeInput
            },
            {'label': _('UUID'), 'field': 'uuid'},
            {
                'label': _('Language'),
                'field': lambda x: get_language(language_code=document.language)
            },
        ]

        kwargs['extra_fields'] = extra_fields
        super().__init__(*args, **kwargs)

    class Meta:
        fields = ('document_type', 'description')
        model = Document
