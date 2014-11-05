from __future__ import absolute_import

import logging

from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from acls.api import class_permissions
from common.utils import encapsulate
from documents.models import Document, DocumentType
from documents.signals import post_document_type_change
from navigation.api import register_links, register_model_list_columns
from navigation.links import link_spacer
from project_setup.api import register_setup
from rest_api.classes import APIEndPoint

from .api import get_metadata_string
from .classes import DocumentTypeMetadataTypeManager
from .links import (metadata_add, metadata_edit, metadata_multiple_add,
                    metadata_multiple_edit, metadata_multiple_remove,
                    metadata_remove, metadata_view,
                    setup_document_type_metadata,
                    setup_document_type_metadata_required,
                    setup_metadata_type_create,
                    setup_metadata_type_delete, setup_metadata_type_edit,
                    setup_metadata_type_list)
from .models import DocumentMetadata, MetadataType
from .permissions import (PERMISSION_METADATA_DOCUMENT_ADD,
                          PERMISSION_METADATA_DOCUMENT_EDIT,
                          PERMISSION_METADATA_DOCUMENT_REMOVE,
                          PERMISSION_METADATA_DOCUMENT_VIEW)

logger = logging.getLogger(__name__)


@receiver(post_document_type_change, dispatch_uid='post_post_document_type_change_metadata', sender=Document)
def post_post_document_type_change_metadata(sender, instance, **kwargs):
    logger.debug('received post_document_type_change')
    logger.debug('instance: %s', instance)
    # Delete existing document metadata
    for metadata in instance.metadata.all():
        metadata.delete(enforce_required=False)

    # Add new document type metadata types to document
    for metadata_type in instance.document_type.metadata_type.filter(required=True):
        DocumentMetadata.objects.create(document=instance, metadata_type=metadata_type, value=None)


@property
def document_metadata(document):
    return document.document_metadata.select_related('metadata_type')


DocumentType.add_to_class('metadata_type', DocumentTypeMetadataTypeManager.factory)
Document.add_to_class('metadata', document_metadata)

register_links(['metadata:metadata_add', 'metadata:metadata_edit', 'metadata:metadata_remove', 'metadata:metadata_view'], [metadata_add, metadata_edit, metadata_remove], menu_name='sidebar')
register_links(Document, [metadata_view], menu_name='form_header')
register_links(DocumentType, [setup_document_type_metadata, setup_document_type_metadata_required])
register_links(MetadataType, [setup_metadata_type_edit, setup_metadata_type_delete])
register_links([MetadataType, 'metadata:setup_metadata_type_list', 'metadata:setup_metadata_type_create'], [setup_metadata_type_list, setup_metadata_type_create], menu_name='secondary_menu')
register_links([Document], [link_spacer, metadata_multiple_add, metadata_multiple_edit, metadata_multiple_remove], menu_name='multi_item_links')

register_setup(setup_metadata_type_list)

class_permissions(Document, [
    PERMISSION_METADATA_DOCUMENT_ADD, PERMISSION_METADATA_DOCUMENT_EDIT,
    PERMISSION_METADATA_DOCUMENT_REMOVE, PERMISSION_METADATA_DOCUMENT_VIEW,
])

register_model_list_columns(Document, [
    {
        'name': _(u'Metadata'), 'attribute': encapsulate(lambda x: get_metadata_string(x))
    },
])

APIEndPoint('metadata')
