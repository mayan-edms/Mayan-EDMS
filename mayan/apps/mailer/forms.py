from __future__ import unicode_literals

from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from .settings import (
    setting_document_body_template, setting_document_subject_template,
    setting_link_body_template, setting_link_subject_template
)


class DocumentMailForm(forms.Form):
    def __init__(self, *args, **kwargs):
        as_attachment = kwargs.pop('as_attachment', False)
        super(DocumentMailForm, self).__init__(*args, **kwargs)
        if as_attachment:
            self.fields['subject'].initial = setting_document_subject_template.value
            self.fields['body'].initial = setting_document_body_template.value % {
                'project_title': settings.PROJECT_TITLE,
                'project_website': settings.PROJECT_WEBSITE
            }
        else:
            self.fields['subject'].initial = setting_link_subject_template.value
            self.fields['body'].initial = setting_link_body_template.value % {
                'project_title': settings.PROJECT_TITLE,
                'project_website': settings.PROJECT_WEBSITE
            }
    email = forms.EmailField(label=_('Email address'))
    subject = forms.CharField(label=_('Subject'), required=False)
    body = forms.CharField(
        label=_('Body'), widget=forms.widgets.Textarea(), required=False
    )
