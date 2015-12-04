from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from .models import DocumentType


def create_default_document_type(sender, **kwargs):
    if not DocumentType.objects.count():    
        DocumentType.objects.create(label=_('Default'))
