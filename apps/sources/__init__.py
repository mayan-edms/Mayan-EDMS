from django.utils.translation import ugettext_lazy as _

from navigation.api import register_links, \
    register_model_list_columns, register_multi_item_links, \
    register_sidebar_template

from sources.staging import StagingFile
from sources.models import WebForm, StagingFolder, SourceTransformation

staging_file_preview = {'text': _(u'preview'), 'class': 'fancybox-noscaling', 'view': 'staging_file_preview', 'args': ['source.source_type', 'source.pk', 'object.id'], 'famfam': 'zoom'}
staging_file_delete = {'text': _(u'delete'), 'view': 'staging_file_delete', 'args': ['source.source_type', 'source.pk', 'object.id'], 'famfam': 'delete', 'keep_query': True}

setup_web_form_list = {'text': _(u'web forms'), 'view': 'setup_web_form_list', 'famfam': 'application_form', 'children_classes': [WebForm]}
setup_staging_folder_list = {'text': _(u'staging folders'), 'view': 'setup_staging_folder_list', 'famfam': 'folder_magnify', 'children_classes': [StagingFolder]}

setup_source_edit = {'text': _(u'edit'), 'view': 'setup_source_edit', 'args': ['source.source_type', 'source.pk'], 'famfam': 'application_form_edit'}
setup_source_delete = {'text': _(u'delete'), 'view': 'setup_source_delete', 'args': ['source.source_type', 'source.pk'], 'famfam': 'application_form_delete'}
setup_source_create = {'text': _(u'add new'), 'view': 'setup_source_create', 'args': 'source_type', 'famfam': 'application_form_add'}

setup_source_transformation_list = {'text': _(u'transformations'), 'view': 'setup_source_transformation_list', 'args': ['source.source_type', 'source.pk'], 'famfam': 'shape_move_front'}
setup_source_transformation_create = {'text': _(u'add transformation'), 'view': 'setup_source_transformation_create', 'args': ['source.source_type', 'source.pk'], 'famfam': 'shape_square_add'}
setup_source_transformation_edit = {'text': _(u'edit'), 'view': 'setup_source_transformation_edit', 'args': 'transformation.pk', 'famfam': 'shape_square_edit'}
setup_source_transformation_delete = {'text': _(u'delete'), 'view': 'setup_source_transformation_delete', 'args': 'transformation.pk', 'famfam': 'shape_square_delete'}

source_list = {'text': _(u'Document sources'), 'view': 'setup_web_form_list', 'famfam': 'page_add', 'children_url_regex': [r'sources/setup']}

register_links(StagingFile, [staging_file_preview, staging_file_delete])

register_links(SourceTransformation, [setup_source_transformation_edit, setup_source_transformation_delete])

register_links(['setup_web_form_list', 'setup_staging_folder_list', 'setup_source_create'], [setup_web_form_list, setup_staging_folder_list], menu_name='form_header')

register_links(WebForm, [setup_web_form_list, setup_staging_folder_list], menu_name='form_header')
register_links(WebForm, [setup_source_transformation_list, setup_source_edit, setup_source_delete])

register_links(['setup_web_form_list', 'setup_staging_folder_list', 'setup_source_edit', 'setup_source_delete', 'setup_source_create'], [setup_source_create], menu_name='sidebar')

register_links(StagingFolder, [setup_web_form_list, setup_staging_folder_list], menu_name='form_header')
register_links(StagingFolder, [setup_source_transformation_list, setup_source_edit, setup_source_delete])

register_links(['setup_source_transformation_create', 'setup_source_transformation_edit', 'setup_source_transformation_delete', 'setup_source_transformation_list'], [setup_source_transformation_create], menu_name='sidebar')

source_views = ['setup_web_form_list', 'setup_staging_folder_list', 'setup_source_edit', 'setup_source_delete', 'setup_source_create', 'setup_source_transformation_list', 'setup_source_transformation_edit', 'setup_source_transformation_delete', 'setup_source_transformation_create']
