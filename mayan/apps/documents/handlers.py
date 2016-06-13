from __future__ import unicode_literals

from django.apps import apps

from .literals import DEFAULT_DOCUMENT_TYPE_LABEL
from .signals import post_initial_document_type


def create_default_document_type(sender, **kwargs):
    DocumentType = apps.get_model(
        app_label='documents', model_name='DocumentType'
    )

    if not DocumentType.on_organization.count():
        document_type = DocumentType.objects.create(
            label=DEFAULT_DOCUMENT_TYPE_LABEL
        )
        post_initial_document_type.send(
            sender=DocumentType, instance=document_type
        )
