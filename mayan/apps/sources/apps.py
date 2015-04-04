from __future__ import absolute_import, unicode_literals

from django import apps
from django.utils.translation import ugettext_lazy as _

from common import menu_front_page, menu_setup
from common.utils import encapsulate
from documents.models import Document
from main import MissingItem
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

        register_model_list_columns(StagingFile, [
            {
                'name': _('Thumbnail'), 'attribute':
                encapsulate(lambda x: staging_file_thumbnail(x, gallery_name='sources:staging_list', title=x.filename, size='100'))
            },
        ])

        # TODO: convert
        #register_links([StagingFile], [staging_file_delete])
        #register_links([Source, 'sources:setup_source_list', 'sources:setup_source_create'], [setup_sources, setup_source_create_webform, setup_source_create_staging_folder, setup_source_create_pop3_email, setup_source_create_imap_email, setup_source_create_watch_folder], menu_name='secondary_menu')
        #register_links([Source], [setup_source_edit, setup_source_transformation_list, setup_source_delete])
        #register_links(SourceTransformation, [setup_source_transformation_edit, setup_source_transformation_delete])
        #register_links([SourceTransformation, 'sources:setup_source_transformation_create', 'sources:setup_source_transformation_list'], [setup_source_transformation_create], menu_name='sidebar')
        #register_links(['documents:document_version_list', 'documents:upload_version', 'documents:document_version_revert'], [upload_version], menu_name='sidebar')
        #register_links(Document, [document_create_siblings])

        menu_setup.bind_links(links=[link_setup_sources])

        menu_front_page.bind_links(links=[link_document_create_multiple])

