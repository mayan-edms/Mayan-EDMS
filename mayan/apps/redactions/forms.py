from __future__ import unicode_literals

import base64

from PIL import Image

from django import forms
from django.utils.encoding import force_unicode
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.widgets import TextAreaDiv
from mayan.apps.converter.models import Transformation
#from metadata.models import MetadataType

from .models import Redaction


class RedactionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.document_page = kwargs.pop('document_page', None)
        super(RedactionForm, self).__init__(*args, **kwargs)
        #if not self.document_type and self.instance:
        #    self.document_type = self.instance.document_type

    class Meta:
        #fields = ('label', 'slug', 'enabled')
        fields = ()
        model = Redaction


class RedactionCoordinatesForm(forms.ModelForm):
    class Meta:
        #fields = ('label', 'slug', 'enabled', 'top', 'left', 'right', 'bottom')
        #fields = ('top', 'left', 'right', 'bottom')
        fields = ('arguments',)
        model = Redaction
        widgets = {
            #'top': forms.widgets.HiddenInput,
            #'left': forms.widgets.HiddenInput,
            #'right': forms.widgets.HiddenInput,
            #'bottom': forms.widgets.HiddenInput,
        }
