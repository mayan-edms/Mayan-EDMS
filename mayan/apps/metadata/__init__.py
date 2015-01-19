from __future__ import unicode_literals

import logging

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from acls.api import class_permissions
from common.classes import ModelAttribute
from common.utils import encapsulate
from documents.models import Document, DocumentType
from documents.signals import post_document_type_change
from navigation.api import register_links, register_model_list_columns
from navigation.links import link_spacer
from project_setup.api import register_setup
from project_tools.api import register_tool
from rest_api.classes import APIEndPoint

from .api import get_metadata_string
from .classes import DocumentMetadataHelper
from .links import (
    metadata_add, metadata_edit, metadata_multiple_add, metadata_multiple_edit,
    metadata_multiple_remove, metadata_remove, metadata_view,
    setup_document_type_metadata, setup_document_type_metadata_required,
    setup_metadata_type_create, setup_metadata_type_delete,
    setup_metadata_type_edit, setup_metadata_type_list,
    link_documents_missing_required_metadata
)
from .models import DocumentMetadata, DocumentTypeMetadataType, MetadataType
from .permissions import (
    PERMISSION_METADATA_DOCUMENT_ADD, PERMISSION_METADATA_DOCUMENT_EDIT,
    PERMISSION_METADATA_DOCUMENT_REMOVE, PERMISSION_METADATA_DOCUMENT_VIEW
)
from .tasks import task_add_required_metadata_type, task_remove_metadata_type

logger = logging.getLogger(__name__)


@receiver(post_save, dispatch_uid='post_document_type_metadata_type_add', sender=DocumentTypeMetadataType)
def post_document_type_metadata_type_add(sender, instance, created, **kwargs):
    logger.debug('instance: %s', instance)

    if created and instance.required:
        task_add_required_metadata_type.apply_async(kwargs={'document_type_id': instance.document_type.pk, 'metadata_type_id': instance.metadata_type.pk}, queue='metadata')


@receiver(post_delete, dispatch_uid='post_document_type_metadata_type_delete', sender=DocumentTypeMetadataType)
def post_document_type_metadata_type_delete(sender, instance, **kwargs):
    logger.debug('instance: %s', instance)
    task_remove_metadata_type.apply_async(kwargs={'document_type_id': instance.document_type.pk, 'metadata_type_id': instance.metadata_type.pk}, queue='metadata')


@receiver(post_document_type_change, dispatch_uid='post_post_document_type_change_metadata', sender=Document)
def post_post_document_type_change_metadata(sender, instance, **kwargs):
    logger.debug('received post_document_type_change')
    logger.debug('instance: %s', instance)
    # Delete existing document metadata
    for metadata in instance.metadata.all():
        metadata.delete(enforce_required=False)

    # Add new document type metadata types to document
    for document_type_metadata_type in instance.document_type.metadata.filter(required=True):
        DocumentMetadata.objects.create(document=instance, metadata_type=document_type_metadata_type.metadata_type, value=None)


Document.add_to_class('metadata_value_of', DocumentMetadataHelper.constructor)

register_links(['metadata:metadata_add', 'metadata:metadata_edit', 'metadata:metadata_remove', 'metadata:metadata_view'], [metadata_add, metadata_edit, metadata_remove], menu_name='sidebar')
register_links(Document, [metadata_view], menu_name='form_header')
register_links([Document], [metadata_multiple_add, metadata_multiple_edit, metadata_multiple_remove, link_spacer], menu_name='multi_item_links')
register_links(DocumentType, [setup_document_type_metadata, setup_document_type_metadata_required])
register_links(MetadataType, [setup_metadata_type_edit, setup_metadata_type_delete])
register_links([MetadataType, 'metadata:setup_metadata_type_list', 'metadata:setup_metadata_type_create'], [setup_metadata_type_list, setup_metadata_type_create], menu_name='secondary_menu')

register_setup(setup_metadata_type_list)
register_tool(link_documents_missing_required_metadata)

class_permissions(Document, [
    PERMISSION_METADATA_DOCUMENT_ADD, PERMISSION_METADATA_DOCUMENT_EDIT,
    PERMISSION_METADATA_DOCUMENT_REMOVE, PERMISSION_METADATA_DOCUMENT_VIEW,
])

register_model_list_columns(Document, [
    {
        'name': _('Metadata'), 'attribute': encapsulate(lambda x: get_metadata_string(x))
    },
])

APIEndPoint('metadata')
ModelAttribute(Document, 'metadata__metadata_type__name', label=_('Metadata type name'), type_name='query')
ModelAttribute(Document, 'metadata__value', label=_('Metadata type value'), type_name='query')
ModelAttribute(Document, 'metadata', type_name='related', description=_('Queryset containing a MetadataType instance reference and a value for that metadata type'))
ModelAttribute(Document, 'metadata_value_of', label=_('Value of a metadata'), description=_('Return the value of a specific document metadata'), type_name=['property', 'indexing'])
