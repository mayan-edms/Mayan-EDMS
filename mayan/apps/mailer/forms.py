from __future__ import unicode_literals

from django import forms
from django.utils.translation import ugettext as _

from .settings import (
    DOCUMENT_BODY_TEMPLATE, DOCUMENT_SUBJECT_TEMPLATE, LINK_BODY_TEMPLATE,
    LINK_SUBJECT_TEMPLATE
)


class DocumentMailForm(forms.Form):
    def __init__(self, *args, **kwargs):
        as_attachment = kwargs.pop('as_attachment', False)
        super(DocumentMailForm, self).__init__(*args, **kwargs)
        if as_attachment:
            self.fields['subject'].initial = DOCUMENT_SUBJECT_TEMPLATE
            self.fields['body'].initial = DOCUMENT_BODY_TEMPLATE
        else:
            self.fields['subject'].initial = LINK_SUBJECT_TEMPLATE
            self.fields['body'].initial = LINK_BODY_TEMPLATE

    email = forms.EmailField(label=_('Email address'))
    subject = forms.CharField(label=_('Subject'), required=False)
    body = forms.CharField(label=_('Body'), widget=forms.widgets.Textarea(), required=False)
