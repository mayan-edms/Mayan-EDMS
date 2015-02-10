from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from documents.permissions import (
    PERMISSION_DOCUMENT_CREATE, PERMISSION_DOCUMENT_NEW_VERSION
)

from .literals import (
    SOURCE_CHOICE_WEB_FORM, SOURCE_CHOICE_EMAIL_IMAP, SOURCE_CHOICE_EMAIL_POP3,
    SOURCE_CHOICE_STAGING, SOURCE_CHOICE_WATCH
)
from .permissions import (
    PERMISSION_SOURCES_SETUP_CREATE, PERMISSION_SOURCES_SETUP_DELETE,
    PERMISSION_SOURCES_SETUP_EDIT, PERMISSION_SOURCES_SETUP_VIEW
)

document_create_multiple = {'text': _('Upload new documents'), 'view': 'sources:document_create_multiple', 'icon': 'main/icons/page_add.png', 'famfam': 'page_add', 'permissions': [PERMISSION_DOCUMENT_CREATE]}
document_create_siblings = {'text': _('Clone'), 'view': 'sources:document_create_siblings', 'args': 'object.id', 'famfam': 'page_copy', 'permissions': [PERMISSION_DOCUMENT_CREATE]}

staging_file_delete = {'text': _('Delete'), 'view': 'sources:staging_file_delete', 'args': ['source.pk', 'object.encoded_filename'], 'famfam': 'delete', 'keep_query': True, 'permissions': [PERMISSION_DOCUMENT_NEW_VERSION, PERMISSION_DOCUMENT_CREATE]}

setup_sources = {'text': _('Sources'), 'view': 'sources:setup_source_list', 'famfam': 'application_form', 'icon': 'main/icons/application_form.png', 'permissions': [PERMISSION_SOURCES_SETUP_VIEW]}
setup_source_create_webform = {'text': _('Add new webform source'), 'view': 'sources:setup_source_create', 'args': '"%s"' % SOURCE_CHOICE_WEB_FORM, 'famfam': 'application_form_add', 'permissions': [PERMISSION_SOURCES_SETUP_CREATE], 'conditional_highlight': lambda context: context.get('source_type') == SOURCE_CHOICE_WEB_FORM and 'source' not in context}
setup_source_create_staging_folder = {'text': _('Add new staging folder'), 'view': 'sources:setup_source_create', 'args': '"%s"' % SOURCE_CHOICE_STAGING, 'famfam': 'folder_camera', 'permissions': [PERMISSION_SOURCES_SETUP_CREATE], 'conditional_highlight': lambda context: context.get('source_type') == SOURCE_CHOICE_STAGING and 'source' not in context}
setup_source_create_watch_folder = {'text': _('Add new watch folder'), 'view': 'sources:setup_source_create', 'args': '"%s"' % SOURCE_CHOICE_WATCH, 'famfam': 'folder_magnify', 'permissions': [PERMISSION_SOURCES_SETUP_CREATE], 'conditional_highlight': lambda context: context.get('source_type') == SOURCE_CHOICE_WATCH and 'source' not in context}
setup_source_create_pop3_email = {'text': _('Add new POP3 email'), 'view': 'sources:setup_source_create', 'args': '"%s"' % SOURCE_CHOICE_EMAIL_POP3, 'famfam': 'email', 'permissions': [PERMISSION_SOURCES_SETUP_CREATE], 'conditional_highlight': lambda context: context.get('source_type') == SOURCE_CHOICE_EMAIL_POP3 and 'source' not in context}
setup_source_create_imap_email = {'text': _('Add new IMAP email'), 'view': 'sources:setup_source_create', 'args': '"%s"' % SOURCE_CHOICE_EMAIL_IMAP, 'famfam': 'email', 'permissions': [PERMISSION_SOURCES_SETUP_CREATE], 'conditional_highlight': lambda context: context.get('source_type') == SOURCE_CHOICE_EMAIL_IMAP and 'source' not in context}
setup_source_delete = {'text': _('Delete'), 'view': 'sources:setup_source_delete', 'args': ['source.pk'], 'famfam': 'application_form_delete', 'permissions': [PERMISSION_SOURCES_SETUP_DELETE]}
setup_source_edit = {'text': _('Edit'), 'view': 'sources:setup_source_edit', 'args': ['source.pk'], 'famfam': 'application_form_edit', 'permissions': [PERMISSION_SOURCES_SETUP_EDIT]}

setup_source_transformation_list = {'text': _('Transformations'), 'view': 'sources:setup_source_transformation_list', 'args': ['source.pk'], 'famfam': 'shape_move_front', 'permissions': [PERMISSION_SOURCES_SETUP_EDIT]}
setup_source_transformation_create = {'text': _('Add transformation'), 'view': 'sources:setup_source_transformation_create', 'args': ['source.pk'], 'famfam': 'shape_square_add', 'permissions': [PERMISSION_SOURCES_SETUP_EDIT]}
setup_source_transformation_edit = {'text': _('Edit'), 'view': 'sources:setup_source_transformation_edit', 'args': 'transformation.pk', 'famfam': 'shape_square_edit', 'permissions': [PERMISSION_SOURCES_SETUP_EDIT]}
setup_source_transformation_delete = {'text': _('Delete'), 'view': 'sources:setup_source_transformation_delete', 'args': 'transformation.pk', 'famfam': 'shape_square_delete', 'permissions': [PERMISSION_SOURCES_SETUP_EDIT]}

source_list = {'text': _('Document sources'), 'view': 'sources:setup_web_form_list', 'famfam': 'page_add', 'permissions': [PERMISSION_SOURCES_SETUP_VIEW]}

upload_version = {'text': _('Upload new version'), 'view': 'sources:upload_version', 'args': 'object.pk', 'famfam': 'page_add', 'permissions': [PERMISSION_DOCUMENT_NEW_VERSION]}
