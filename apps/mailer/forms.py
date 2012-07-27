from __future__ import absolute_import

from django import forms
from django.utils.translation import ugettext as _

from .conf import settings


class DocumentMailForm(forms.Form):
    def __init__(self, *args, **kwargs):
        as_attachment = kwargs.pop('as_attachment', False)
        super(DocumentMailForm, self).__init__(*args, **kwargs)
        if as_attachment:
            self.fields['subject'].initial = settings.DOCUMENT_SUBJECT_TEMPLATE
            self.fields['body'].initial = settings.DOCUMENT_BODY_TEMPLATE
        else:
            self.fields['subject'].initial = settings.LINK_SUBJECT_TEMPLATE
            self.fields['body'].initial = settings.LINK_BODY_TEMPLATE

    email = forms.EmailField(label=_(u'Email address'))
    subject = forms.CharField(label=_(u'Subject'), required=False)
    body = forms.CharField(label=_(u'Body'), widget=forms.widgets.Textarea(), required=False)
