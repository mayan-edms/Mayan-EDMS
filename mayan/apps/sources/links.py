from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from converter.permissions import PERMISSION_TRANSFORMATION_VIEW
from documents.permissions import (
    PERMISSION_DOCUMENT_CREATE, PERMISSION_DOCUMENT_NEW_VERSION
)
from navigation import Link

from .literals import (
    SOURCE_CHOICE_WEB_FORM, SOURCE_CHOICE_EMAIL_IMAP, SOURCE_CHOICE_EMAIL_POP3,
    SOURCE_CHOICE_STAGING, SOURCE_CHOICE_WATCH
)
from .permissions import (
    PERMISSION_SOURCES_SETUP_CREATE, PERMISSION_SOURCES_SETUP_DELETE,
    PERMISSION_SOURCES_SETUP_EDIT, PERMISSION_SOURCES_SETUP_VIEW
)


link_document_create_multiple = Link(icon='fa fa-upload', permissions=[PERMISSION_DOCUMENT_CREATE], text=_('New document'), view='sources:document_create_multiple')
link_document_create_siblings = Link(permissions=[PERMISSION_DOCUMENT_CREATE], text=_('Clone'), view='sources:document_create_siblings', args='object.id')
link_setup_sources = Link(icon='fa fa-upload', permissions=[PERMISSION_SOURCES_SETUP_VIEW], text=_('Sources'), view='sources:setup_source_list')
link_setup_source_create_imap_email = Link(permissions=[PERMISSION_SOURCES_SETUP_CREATE], text=_('Add new IMAP email'), view='sources:setup_source_create', args='"%s"' % SOURCE_CHOICE_EMAIL_IMAP)
link_setup_source_create_pop3_email = Link(permissions=[PERMISSION_SOURCES_SETUP_CREATE], text=_('Add new POP3 email'), view='sources:setup_source_create', args='"%s"' % SOURCE_CHOICE_EMAIL_POP3)
link_setup_source_create_staging_folder = Link(permissions=[PERMISSION_SOURCES_SETUP_CREATE], text=_('Add new staging folder'), view='sources:setup_source_create', args='"%s"' % SOURCE_CHOICE_STAGING)
link_setup_source_create_watch_folder = Link(permissions=[PERMISSION_SOURCES_SETUP_CREATE], text=_('Add new watch folder'), view='sources:setup_source_create', args='"%s"' % SOURCE_CHOICE_WATCH)
link_setup_source_create_webform = Link(permissions=[PERMISSION_SOURCES_SETUP_CREATE], text=_('Add new webform source'), view='sources:setup_source_create', args='"%s"' % SOURCE_CHOICE_WEB_FORM)
link_setup_source_delete = Link(permissions=[PERMISSION_SOURCES_SETUP_DELETE], tags='dangerous', text=_('Delete'), view='sources:setup_source_delete', args=['resolved_object.pk'])
link_setup_source_edit = Link(text=_('Edit'), view='sources:setup_source_edit', args=['resolved_object.pk'], permissions=[PERMISSION_SOURCES_SETUP_EDIT])
link_source_list = Link(permissions=[PERMISSION_SOURCES_SETUP_VIEW], text=_('Document sources'), view='sources:setup_web_form_list')
link_staging_file_delete = Link(keep_query=True, permissions=[PERMISSION_DOCUMENT_NEW_VERSION, PERMISSION_DOCUMENT_CREATE], tags='dangerous', text=_('Delete'), view='sources:staging_file_delete', args=['source.pk', 'object.encoded_filename'])
link_upload_version = Link(permissions=[PERMISSION_DOCUMENT_NEW_VERSION], text=_('Upload new version'), view='sources:upload_version', args='object.pk')
link_setup_source_logs = Link(text=_('Logs'), view='sources:setup_source_logs', args=['resolved_object.pk'], permissions=[PERMISSION_SOURCES_SETUP_VIEW])

