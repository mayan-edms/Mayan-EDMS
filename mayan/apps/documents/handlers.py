from __future__ import unicode_literals

from django.apps import apps
from django.utils.translation import ugettext_lazy as _


def create_default_document_type(sender, **kwargs):
    DocumentType = apps.get_model(
        app_label='documents', model_name='DocumentType'
    )

    if not DocumentType.objects.count():
        DocumentType.objects.create(label=_('Default'))
