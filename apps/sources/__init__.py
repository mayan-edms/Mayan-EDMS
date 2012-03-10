from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation.api import (register_links,
    register_model_list_columns)
from common.utils import encapsulate
from project_setup.api import register_setup
from documents.permissions import (PERMISSION_DOCUMENT_NEW_VERSION, 
    PERMISSION_DOCUMENT_CREATE)
from scheduler.api import register_interval_job

from .staging import StagingFile
from .models import (WebForm, StagingFolder, SourceTransformation,
    WatchFolder, POP3Email)
from .widgets import staging_file_thumbnail
from .permissions import (PERMISSION_SOURCES_SETUP_VIEW,
    PERMISSION_SOURCES_SETUP_EDIT, PERMISSION_SOURCES_SETUP_DELETE,
    PERMISSION_SOURCES_SETUP_CREATE)
from .tasks import task_fetch_pop3_emails
from .conf.settings import POP3_EMAIL_PROCESSING_INTERVAL

staging_file_preview = {'text': _(u'preview'), 'class': 'fancybox-noscaling', 'view': 'staging_file_preview', 'args': ['source.source_type', 'source.pk', 'object.id'], 'famfam': 'zoom', 'permissions': [PERMISSION_DOCUMENT_NEW_VERSION, PERMISSION_DOCUMENT_CREATE]}
staging_file_delete = {'text': _(u'delete'), 'view': 'staging_file_delete', 'args': ['source.source_type', 'source.pk', 'object.id'], 'famfam': 'delete', 'keep_query': True, 'permissions': [PERMISSION_DOCUMENT_NEW_VERSION, PERMISSION_DOCUMENT_CREATE]}

setup_sources = {'text': _(u'sources'), 'view': 'setup_web_form_list', 'famfam': 'application_form', 'icon': 'application_form.png', 'children_classes': [WebForm], 'permissions': [PERMISSION_SOURCES_SETUP_VIEW], 'children_view_regex': [r'setup_web_form', r'setup_staging_folder', r'setup_source_']}
setup_web_form_list = {'text': _(u'web forms'), 'view': 'setup_web_form_list', 'famfam': 'application_form', 'icon': 'application_form.png', 'children_classes': [WebForm], 'permissions': [PERMISSION_SOURCES_SETUP_VIEW]}
setup_staging_folder_list = {'text': _(u'staging folders'), 'view': 'setup_staging_folder_list', 'famfam': 'folder_camera', 'children_classes': [StagingFolder], 'permissions': [PERMISSION_SOURCES_SETUP_VIEW]}
setup_watch_folder_list = {'text': _(u'watch folders'), 'view': 'setup_watch_folder_list', 'famfam': 'folder_magnify', 'children_classes': [WatchFolder], 'permissions': [PERMISSION_SOURCES_SETUP_VIEW]}
setup_pop3_email_list = {'text': _(u'POP3 email'), 'view': 'setup_pop3_email_list', 'famfam': 'email', 'children_classes': [POP3Email], 'permissions': [PERMISSION_SOURCES_SETUP_VIEW]}

setup_source_edit = {'text': _(u'edit'), 'view': 'setup_source_edit', 'args': ['source.source_type', 'source.pk'], 'famfam': 'application_form_edit', 'permissions': [PERMISSION_SOURCES_SETUP_EDIT]}
setup_source_delete = {'text': _(u'delete'), 'view': 'setup_source_delete', 'args': ['source.source_type', 'source.pk'], 'famfam': 'application_form_delete', 'permissions': [PERMISSION_SOURCES_SETUP_DELETE]}
setup_source_create = {'text': _(u'add new source'), 'view': 'setup_source_create', 'args': 'source_type', 'famfam': 'application_form_add', 'permissions': [PERMISSION_SOURCES_SETUP_CREATE]}

setup_source_transformation_list = {'text': _(u'transformations'), 'view': 'setup_source_transformation_list', 'args': ['source.source_type', 'source.pk'], 'famfam': 'shape_move_front', 'permissions': [PERMISSION_SOURCES_SETUP_EDIT]}
setup_source_transformation_create = {'text': _(u'add transformation'), 'view': 'setup_source_transformation_create', 'args': ['source.source_type', 'source.pk'], 'famfam': 'shape_square_add', 'permissions': [PERMISSION_SOURCES_SETUP_EDIT]}
setup_source_transformation_edit = {'text': _(u'edit'), 'view': 'setup_source_transformation_edit', 'args': 'transformation.pk', 'famfam': 'shape_square_edit', 'permissions': [PERMISSION_SOURCES_SETUP_EDIT]}
setup_source_transformation_delete = {'text': _(u'delete'), 'view': 'setup_source_transformation_delete', 'args': 'transformation.pk', 'famfam': 'shape_square_delete', 'permissions': [PERMISSION_SOURCES_SETUP_EDIT]}

source_list = {'text': _(u'Document sources'), 'view': 'setup_web_form_list', 'famfam': 'page_add', 'children_url_regex': [r'sources/setup'], 'permissions': [PERMISSION_SOURCES_SETUP_VIEW]}

upload_version = {'text': _(u'upload new version'), 'view': 'upload_version', 'args': 'object.pk', 'famfam': 'page_add', 'permissions': [PERMISSION_DOCUMENT_NEW_VERSION]}

register_links(StagingFile, [staging_file_delete])

register_links(SourceTransformation, [setup_source_transformation_edit, setup_source_transformation_delete])

#register_links(['setup_web_form_list', 'setup_staging_folder_list', 'setup_watch_folder_list', 'setup_source_create'], [setup_web_form_list, setup_staging_folder_list, setup_watch_folder_list], menu_name='form_header')
register_links(['setup_pop3_email_list', 'setup_web_form_list', 'setup_staging_folder_list', 'setup_watch_folder_list', 'setup_source_create'], [setup_web_form_list, setup_staging_folder_list, setup_pop3_email_list], menu_name='form_header')

#register_links(WebForm, [setup_web_form_list, setup_staging_folder_list, setup_watch_folder_list], menu_name='form_header')
register_links(WebForm, [setup_web_form_list, setup_staging_folder_list, setup_pop3_email_list], menu_name='form_header')
register_links(WebForm, [setup_source_transformation_list, setup_source_edit, setup_source_delete])

register_links(['setup_web_form_list', 'setup_staging_folder_list', 'setup_watch_folder_list', 'setup_source_edit', 'setup_source_delete', 'setup_source_create', 'setup_pop3_email_list'], [setup_sources, setup_source_create], menu_name='sidebar')

#register_links(StagingFolder, [setup_web_form_list, setup_staging_folder_list, setup_watch_folder_list], menu_name='form_header')
register_links(StagingFolder, [setup_web_form_list, setup_staging_folder_list, setup_pop3_email_list], menu_name='form_header')
register_links(StagingFolder, [setup_source_transformation_list, setup_source_edit, setup_source_delete])

register_links(POP3Email, [setup_web_form_list, setup_staging_folder_list, setup_pop3_email_list], menu_name='form_header')
register_links(POP3Email, [setup_source_transformation_list, setup_source_edit, setup_source_delete])

register_links(WatchFolder, [setup_web_form_list, setup_staging_folder_list, setup_watch_folder_list], menu_name='form_header')
register_links(WatchFolder, [setup_source_transformation_list, setup_source_edit, setup_source_delete])

# Document version
register_links(['document_version_list', 'upload_version', 'document_version_revert'], [upload_version], menu_name='sidebar')

register_links(['setup_source_transformation_create', 'setup_source_transformation_edit', 'setup_source_transformation_delete', 'setup_source_transformation_list'], [setup_source_transformation_create], menu_name='sidebar')

source_views = ['setup_web_form_list', 'setup_staging_folder_list', 'setup_watch_folder_list', 'setup_source_edit', 'setup_source_delete', 'setup_source_create', 'setup_source_transformation_list', 'setup_source_transformation_edit', 'setup_source_transformation_delete', 'setup_source_transformation_create']

register_model_list_columns(StagingFile, [
        {'name':_(u'thumbnail'), 'attribute':
            encapsulate(lambda x: staging_file_thumbnail(x))
        },
    ])

register_setup(setup_sources)

register_interval_job('task_fetch_pop3_emails', _(u'Connects to the POP3 email sources and fetches the attached documents.'), task_fetch_pop3_emails, seconds=POP3_EMAIL_PROCESSING_INTERVAL)
