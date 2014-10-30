from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from common.utils import encapsulate
from documents.models import Document
from navigation.api import register_links, register_model_list_columns
from project_setup.api import register_setup
from rest_api.classes import APIEndPoint

from .classes import StagingFile
from .links import (document_create_multiple, document_create_siblings,
                    setup_sources, setup_source_create_imap_email,
                    setup_source_create_pop3_email,
                    setup_source_create_watch_folder,
                    setup_source_create_webform,
                    setup_source_create_staging_folder,
                    setup_source_delete, setup_source_edit,
                    setup_source_transformation_create,
                    setup_source_transformation_delete,
                    setup_source_transformation_edit,
                    setup_source_transformation_list,
                    staging_file_delete, upload_version)
from .models import Source, SourceTransformation
from .widgets import staging_file_thumbnail

register_links([StagingFile], [staging_file_delete])

register_links([Source, 'sources:setup_source_list', 'sources:setup_source_create'], [setup_sources, setup_source_create_webform, setup_source_create_staging_folder, setup_source_create_pop3_email, setup_source_create_imap_email, setup_source_create_watch_folder], menu_name='secondary_menu')
register_links([Source], [setup_source_edit, setup_source_transformation_list, setup_source_delete])

register_links(SourceTransformation, [setup_source_transformation_edit, setup_source_transformation_delete])
register_links(['sources:setup_source_transformation_create', 'sources:setup_source_transformation_edit', 'sources:setup_source_transformation_delete', 'sources:setup_source_transformation_list'], [setup_source_transformation_create], menu_name='sidebar')

# Document version
register_links(['documents:document_version_list', 'documents:upload_version', 'documents:document_version_revert'], [upload_version], menu_name='sidebar')

register_model_list_columns(StagingFile, [
    {
        'name': _(u'Thumbnail'), 'attribute':
        encapsulate(lambda x: staging_file_thumbnail(x, gallery_name='sources:staging_list', title=x.filename, size='100'))
    },
])

register_setup(setup_sources)

register_links([Document, 'documents:document_list_recent', 'documents:document_list', 'sources:document_create', 'sources:document_create_multiple', 'sources:upload_interactive', 'sources:staging_file_delete'], [document_create_multiple], menu_name='secondary_menu')
register_links(Document, [document_create_siblings])

APIEndPoint('sources')
