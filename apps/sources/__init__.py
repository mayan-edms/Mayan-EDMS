from django.utils.translation import ugettext_lazy as _

from navigation.api import register_links, \
    register_model_list_columns
from permissions.api import register_permission, set_namespace_title

from sources.staging import StagingFile
from sources.models import WebForm, StagingFolder, SourceTransformation, \
    WatchFolder
from sources.widgets import staging_file_thumbnail

PERMISSION_SOURCES_SETUP_VIEW = {'namespace': 'sources_setup', 'name': 'sources_setup_view', 'label': _(u'View existing document sources')}
PERMISSION_SOURCES_SETUP_EDIT = {'namespace': 'sources_setup', 'name': 'sources_setup_edit', 'label': _(u'Edit document sources')}
PERMISSION_SOURCES_SETUP_DELETE = {'namespace': 'sources_setup', 'name': 'sources_setup_delete', 'label': _(u'Delete document sources')}
PERMISSION_SOURCES_SETUP_CREATE = {'namespace': 'sources_setup', 'name': 'sources_setup_create', 'label': _(u'Create new document sources')}

set_namespace_title('sources_setup', _(u'Sources setup'))
register_permission(PERMISSION_SOURCES_SETUP_VIEW)
register_permission(PERMISSION_SOURCES_SETUP_EDIT)
register_permission(PERMISSION_SOURCES_SETUP_DELETE)
register_permission(PERMISSION_SOURCES_SETUP_CREATE)

staging_file_preview = {'text': _(u'preview'), 'class': 'fancybox-noscaling', 'view': 'staging_file_preview', 'args': ['source.source_type', 'source.pk', 'object.id'], 'famfam': 'zoom'}
staging_file_delete = {'text': _(u'delete'), 'view': 'staging_file_delete', 'args': ['source.source_type', 'source.pk', 'object.id'], 'famfam': 'delete', 'keep_query': True}

setup_web_form_list = {'text': _(u'web forms'), 'view': 'setup_web_form_list', 'famfam': 'application_form', 'children_classes': [WebForm]}
setup_staging_folder_list = {'text': _(u'staging folders'), 'view': 'setup_staging_folder_list', 'famfam': 'folder_camera', 'children_classes': [StagingFolder]}
setup_watch_folder_list = {'text': _(u'watch folders'), 'view': 'setup_watch_folder_list', 'famfam': 'folder_magnify', 'children_classes': [WatchFolder]}

setup_source_edit = {'text': _(u'edit'), 'view': 'setup_source_edit', 'args': ['source.source_type', 'source.pk'], 'famfam': 'application_form_edit'}
setup_source_delete = {'text': _(u'delete'), 'view': 'setup_source_delete', 'args': ['source.source_type', 'source.pk'], 'famfam': 'application_form_delete'}
setup_source_create = {'text': _(u'add new source'), 'view': 'setup_source_create', 'args': 'source_type', 'famfam': 'application_form_add'}

setup_source_transformation_list = {'text': _(u'transformations'), 'view': 'setup_source_transformation_list', 'args': ['source.source_type', 'source.pk'], 'famfam': 'shape_move_front'}
setup_source_transformation_create = {'text': _(u'add transformation'), 'view': 'setup_source_transformation_create', 'args': ['source.source_type', 'source.pk'], 'famfam': 'shape_square_add'}
setup_source_transformation_edit = {'text': _(u'edit'), 'view': 'setup_source_transformation_edit', 'args': 'transformation.pk', 'famfam': 'shape_square_edit'}
setup_source_transformation_delete = {'text': _(u'delete'), 'view': 'setup_source_transformation_delete', 'args': 'transformation.pk', 'famfam': 'shape_square_delete'}

source_list = {'text': _(u'Document sources'), 'view': 'setup_web_form_list', 'famfam': 'page_add', 'children_url_regex': [r'sources/setup']}

register_links(StagingFile, [staging_file_delete])

register_links(SourceTransformation, [setup_source_transformation_edit, setup_source_transformation_delete])

#register_links(['setup_web_form_list', 'setup_staging_folder_list', 'setup_watch_folder_list', 'setup_source_create'], [setup_web_form_list, setup_staging_folder_list, setup_watch_folder_list], menu_name='form_header')
register_links(['setup_web_form_list', 'setup_staging_folder_list', 'setup_watch_folder_list', 'setup_source_create'], [setup_web_form_list, setup_staging_folder_list], menu_name='form_header')

#register_links(WebForm, [setup_web_form_list, setup_staging_folder_list, setup_watch_folder_list], menu_name='form_header')
register_links(WebForm, [setup_web_form_list, setup_staging_folder_list], menu_name='form_header')
register_links(WebForm, [setup_source_transformation_list, setup_source_edit, setup_source_delete])

register_links(['setup_web_form_list', 'setup_staging_folder_list', 'setup_watch_folder_list', 'setup_source_edit', 'setup_source_delete', 'setup_source_create'], [setup_source_create], menu_name='sidebar')

#register_links(StagingFolder, [setup_web_form_list, setup_staging_folder_list, setup_watch_folder_list], menu_name='form_header')
register_links(StagingFolder, [setup_web_form_list, setup_staging_folder_list], menu_name='form_header')
register_links(StagingFolder, [setup_source_transformation_list, setup_source_edit, setup_source_delete])

register_links(WatchFolder, [setup_web_form_list, setup_staging_folder_list, setup_watch_folder_list], menu_name='form_header')
register_links(WatchFolder, [setup_source_transformation_list, setup_source_edit, setup_source_delete])

register_links(['setup_source_transformation_create', 'setup_source_transformation_edit', 'setup_source_transformation_delete', 'setup_source_transformation_list'], [setup_source_transformation_create], menu_name='sidebar')

source_views = ['setup_web_form_list', 'setup_staging_folder_list', 'setup_watch_folder_list', 'setup_source_edit', 'setup_source_delete', 'setup_source_create', 'setup_source_transformation_list', 'setup_source_transformation_edit', 'setup_source_transformation_delete', 'setup_source_transformation_create']

register_model_list_columns(StagingFile, [
        {'name':_(u'thumbnail'), 'attribute':
            lambda x: staging_file_thumbnail(x)
        },
    ])
