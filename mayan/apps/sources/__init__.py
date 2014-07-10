from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from common.utils import encapsulate
from documents.models import Document
from navigation.api import register_links, register_model_list_columns
from project_setup.api import register_setup
from rest_api.classes import APIEndPoint

from .classes import StagingFile
from .links import (document_create_multiple, document_create_siblings,
    staging_file_delete, setup_sources, setup_web_form_list,
    setup_staging_folder_list, setup_watch_folder_list,
    setup_source_edit, setup_source_delete, setup_source_create,
    setup_source_transformation_list, setup_source_transformation_create,
    setup_source_transformation_edit, setup_source_transformation_delete,
    upload_version)
from .models import (WebForm, StagingFolder, SourceTransformation,
    WatchFolder)
from .urls import api_urls
from .widgets import staging_file_thumbnail

register_links([StagingFile], [staging_file_delete])

register_links(SourceTransformation, [setup_source_transformation_edit, setup_source_transformation_delete])

register_links(['setup_web_form_list', 'setup_staging_folder_list', 'setup_watch_folder_list', 'setup_source_create'], [setup_web_form_list, setup_staging_folder_list], menu_name='form_header')

register_links(WebForm, [setup_web_form_list, setup_staging_folder_list], menu_name='form_header')
register_links(WebForm, [setup_source_transformation_list, setup_source_edit, setup_source_delete])

register_links(['setup_web_form_list', 'setup_staging_folder_list', 'setup_watch_folder_list', 'setup_source_edit', 'setup_source_delete', 'setup_source_create'], [setup_sources, setup_source_create], menu_name='sidebar')

register_links(StagingFolder, [setup_web_form_list, setup_staging_folder_list], menu_name='form_header')
register_links(StagingFolder, [setup_source_transformation_list, setup_source_edit, setup_source_delete])

register_links(WatchFolder, [setup_web_form_list, setup_staging_folder_list, setup_watch_folder_list], menu_name='form_header')
register_links(WatchFolder, [setup_source_transformation_list, setup_source_edit, setup_source_delete])

# Document version
register_links(['document_version_list', 'upload_version', 'document_version_revert'], [upload_version], menu_name='sidebar')

register_links(['setup_source_transformation_create', 'setup_source_transformation_edit', 'setup_source_transformation_delete', 'setup_source_transformation_list'], [setup_source_transformation_create], menu_name='sidebar')

source_views = ['setup_web_form_list', 'setup_staging_folder_list', 'setup_watch_folder_list', 'setup_source_edit', 'setup_source_delete', 'setup_source_create', 'setup_source_transformation_list', 'setup_source_transformation_edit', 'setup_source_transformation_delete', 'setup_source_transformation_create']

register_model_list_columns(StagingFile, [
    {
        'name': _(u'thumbnail'), 'attribute':
        encapsulate(lambda x: staging_file_thumbnail(x, gallery_name='staging_list', title=x.filename, size='100'))
    },
])

register_setup(setup_sources)

register_links([Document, 'document_list_recent', 'document_list', 'document_create', 'document_create_multiple', 'upload_interactive', 'staging_file_delete'], [document_create_multiple], menu_name='secondary_menu')
register_links(Document, [document_create_siblings])

endpoint = APIEndPoint('sources')
endpoint.register_urls(api_urls)
endpoint.add_endpoint('stagingfolder-list', _(u'Returns a list of all the staging folders and the files they contain.'))
