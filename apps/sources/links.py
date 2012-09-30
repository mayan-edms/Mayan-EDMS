from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation import Link
from documents.permissions import (PERMISSION_DOCUMENT_NEW_VERSION, 
    PERMISSION_DOCUMENT_CREATE)

from .permissions import (PERMISSION_SOURCES_SETUP_VIEW,
    PERMISSION_SOURCES_SETUP_EDIT, PERMISSION_SOURCES_SETUP_DELETE,
    PERMISSION_SOURCES_SETUP_CREATE)
from .icons import (icon_staging_file_preview, icon_staging_file_delete,
    icon_setup_sources, icon_setup_web_form_list, icon_setup_staging_folder_list,
    icon_setup_watch_folder_list, icon_setup_pop3_email_list,
    icon_setup_imap_email_list, icon_setup_local_scanner_list,
    icon_setup_local_scanners_refresh, icon_setup_source_edit,
    icon_setup_source_delete, icon_setup_source_create,
    icon_setup_source_log_list, icon_source_list, icon_upload_version,
    icon_document_create_multiple, icon_staging_file_preview,
    icon_staging_file_delete, icon_setup_sources, icon_setup_web_form_list,
    icon_setup_staging_folder_list, icon_setup_watch_folder_list,
    icon_setup_pop3_email_list, icon_setup_imap_email_list,
    icon_setup_local_scanner_list, icon_setup_local_scanners_refresh,
    icon_setup_source_edit, icon_setup_source_delete, icon_setup_source_create,
    icon_setup_source_log_list, icon_source_list, icon_upload_version,
    icon_document_create_multiple)

staging_file_preview = Link(text=_(u'preview'), klass='fancybox-noscaling', view='staging_file_preview', args=['source.source_type', 'source.pk', 'object.pk'], icon=icon_staging_file_preview, permissions=[PERMISSION_DOCUMENT_NEW_VERSION, PERMISSION_DOCUMENT_CREATE])
staging_file_delete = Link(text=_(u'delete'), view='staging_file_delete', args=['source.source_type', 'source.pk', 'object.pk'], icon=icon_staging_file_delete, keep_query=True, permissions=[PERMISSION_DOCUMENT_NEW_VERSION, PERMISSION_DOCUMENT_CREATE])

setup_sources = Link(text=_(u'sources'), view='setup_web_form_list', icon=icon_setup_sources, permissions=[PERMISSION_SOURCES_SETUP_VIEW], children_view_regex=[r'setup_web_form', r'setup_staging_folder', r'setup_source_', r'setup_pop3', r'setup_imap'])
setup_web_form_list = Link(text=_(u'web forms'), view='setup_web_form_list', icon=icon_setup_web_form_list, permissions=[PERMISSION_SOURCES_SETUP_VIEW])
setup_staging_folder_list = Link(text=_(u'staging folders'), view='setup_staging_folder_list', icon=icon_setup_staging_folder_list, permissions=[PERMISSION_SOURCES_SETUP_VIEW])
setup_watch_folder_list = Link(text=_(u'watch folders'), view='setup_watch_folder_list', icon=icon_setup_watch_folder_list, permissions=[PERMISSION_SOURCES_SETUP_VIEW])
setup_pop3_email_list = Link(text=_(u'POP3 email'), view='setup_pop3_email_list', icon=icon_setup_pop3_email_list, permissions=[PERMISSION_SOURCES_SETUP_VIEW])
setup_imap_email_list = Link(text=_(u'IMAP email'), view='setup_imap_email_list', icon=icon_setup_imap_email_list, permissions=[PERMISSION_SOURCES_SETUP_VIEW])
setup_local_scanner_list = Link(text=_(u'Local scanner'), view='setup_local_scanner_list', icon=icon_setup_local_scanner_list, permissions=[PERMISSION_SOURCES_SETUP_VIEW])
setup_local_scanners_refresh = Link(text=_(u'Refresh scanner list'), view='scanners_refresh', icon=icon_setup_local_scanners_refresh, permissions=[PERMISSION_SOURCES_SETUP_VIEW])

setup_source_edit = Link(text=_(u'edit'), view='setup_source_edit', args=['source.source_type', 'source.pk'], icon=icon_setup_source_edit, permissions=[PERMISSION_SOURCES_SETUP_EDIT])
setup_source_delete = Link(text=_(u'delete'), view='setup_source_delete', args=['source.source_type', 'source.pk'], icon=icon_setup_source_delete, permissions=[PERMISSION_SOURCES_SETUP_DELETE])
setup_source_create = Link(text=_(u'add new source'), view='setup_source_create', args='source_type', icon=icon_setup_source_create, permissions=[PERMISSION_SOURCES_SETUP_CREATE])
setup_source_log_list = Link(text=_(u'logs'), view='setup_source_log_list', args=['source.source_type', 'source.pk'], icon=icon_setup_source_log_list, permissions=[PERMISSION_SOURCES_SETUP_EDIT])

#setup_source_transformation_list = Link(text=_(u'transformations'), view='setup_source_transformation_list', args=['source.source_type', 'source.pk'], sprite='shape_move_front', permissions=[PERMISSION_SOURCES_SETUP_EDIT])
#setup_source_transformation_create = Link(text=_(u'add transformation'), view='setup_source_transformation_create', args=['source.source_type', 'source.pk'], sprite='shape_square_add', permissions=[PERMISSION_SOURCES_SETUP_EDIT])
#setup_source_transformation_edit = Link(text=_(u'edit'), view='setup_source_transformation_edit', args='transformation.pk', sprite='shape_square_edit', permissions=[PERMISSION_SOURCES_SETUP_EDIT])
#setup_source_transformation_delete = Link(text=_(u'delete'), view='setup_source_transformation_delete', args='transformation.pk', sprite='shape_square_delete', permissions=[PERMISSION_SOURCES_SETUP_EDIT])

source_list = Link(text=_(u'Document sources'), view='setup_web_form_list', icon=icon_source_list, children_url_regex=[r'sources/setup'], permissions=[PERMISSION_SOURCES_SETUP_VIEW])

upload_version = Link(text=_(u'upload new version'), view='upload_version', args='object.pk', icon=icon_upload_version, permissions=[PERMISSION_DOCUMENT_NEW_VERSION])
document_create_multiple = Link(text=_(u'upload new documents'), view='document_create_multiple', icon=icon_document_create_multiple, permissions=[PERMISSION_DOCUMENT_CREATE], children_view_regex=[r'upload_interactive'])
