from django import forms
from django.utils.translation import ugettext as _


class DocumentMailForm(forms.Form):
    email = forms.EmailField(label=_(u'Email address'))
    subject = forms.CharField(label=_(u'Subject'), required=False, initial=_(u'Link for document: {{ document }}'))
    body = forms.CharField(label=_(u'Body'), widget=forms.widgets.Textarea(), required=False, initial=_(u'To access this document click on the following link: <a href="{{ link }}">{{ link }}</a>'))
