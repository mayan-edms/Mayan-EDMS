from __future__ import absolute_import, unicode_literals

from django import apps
from django.utils.translation import ugettext_lazy as _

from common import (
    MissingItem, menu_front_page, menu_object, menu_secondary, menu_sidebar,
    menu_setup
)
from common.utils import encapsulate
from documents.models import Document
from navigation.api import register_model_list_columns
from rest_api.classes import APIEndPoint

from .classes import StagingFile
from .links import (
    link_document_create_multiple, link_document_create_siblings,
    link_setup_sources, link_setup_source_create_imap_email,
    link_setup_source_create_pop3_email,
    link_setup_source_create_watch_folder, link_setup_source_create_webform,
    link_setup_source_create_staging_folder, link_setup_source_delete,
    link_setup_source_edit, link_setup_source_transformation_create,
    link_setup_source_transformation_delete,
    link_setup_source_transformation_edit,
    link_setup_source_transformation_list, link_staging_file_delete,
    link_upload_version
)
from .models import Source, SourceTransformation
from .widgets import staging_file_thumbnail


class SourcesApp(apps.AppConfig):
    name = 'sources'
    verbose_name = _('Sources')

    def ready(self):
        APIEndPoint('sources')
        MissingItem(label=_('Create a document source'), description=_('Document sources are the way in which new documents are feed to Mayan EDMS, create at least a web form source to be able to upload documents from a browser.'), condition=lambda: not Source.objects.exists(), view='sources:setup_source_list')

        menu_front_page.bind_links(links=[link_document_create_multiple])
        menu_object.bind_links(links=[link_document_create_siblings], sources=[Document])
        menu_object.bind_links(links=[link_setup_source_edit, link_setup_source_transformation_list, link_setup_source_delete], sources=[Source])
        menu_object.bind_links(links=[link_setup_source_transformation_edit, link_setup_source_transformation_delete], sources=[SourceTransformation])
        menu_object.bind_links(links=[link_staging_file_delete], sources=[StagingFile])
        menu_secondary.bind_links(links=[link_setup_sources, link_setup_source_create_webform, link_setup_source_create_staging_folder, link_setup_source_create_pop3_email, link_setup_source_create_imap_email, link_setup_source_create_watch_folder], sources=[Source, 'sources:setup_source_list', 'sources:setup_source_create'])
        menu_setup.bind_links(links=[link_setup_sources])
        menu_sidebar.bind_links(links=[link_setup_source_transformation_create], sources=[SourceTransformation, 'sources:setup_source_transformation_create', 'sources:setup_source_transformation_list'])
        menu_sidebar.bind_links(links=[link_upload_version], sources=['documents:document_version_list', 'documents:upload_version', 'documents:document_version_revert'])

        register_model_list_columns(StagingFile, [
            {
                'name': _('Thumbnail'), 'attribute':
                encapsulate(lambda x: staging_file_thumbnail(x, gallery_name='sources:staging_list', title=x.filename, size='100'))
            },
        ])
