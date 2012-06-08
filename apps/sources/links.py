from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation.api import Link
from documents.permissions import (PERMISSION_DOCUMENT_NEW_VERSION, 
    PERMISSION_DOCUMENT_CREATE)
from .permissions import (PERMISSION_SOURCES_SETUP_VIEW,
    PERMISSION_SOURCES_SETUP_EDIT, PERMISSION_SOURCES_SETUP_DELETE,
    PERMISSION_SOURCES_SETUP_CREATE)
from .models import (WebForm, StagingFolder, SourceTransformation,
    WatchFolder, POP3Email, IMAPEmail)
    
staging_file_preview = Link(text=_(u'preview'), klass='fancybox-noscaling', view='staging_file_preview', args=['source.source_type', 'source.pk', 'object.pk'], sprite='zoom', permissions=[PERMISSION_DOCUMENT_NEW_VERSION, PERMISSION_DOCUMENT_CREATE])
staging_file_delete = Link(text=_(u'delete'), view='staging_file_delete', args=['source.source_type', 'source.pk', 'object.pk'], sprite='delete', keep_query=True, permissions=[PERMISSION_DOCUMENT_NEW_VERSION, PERMISSION_DOCUMENT_CREATE])

setup_sources = Link(text=_(u'sources'), view='setup_web_form_list', sprite='application_form', icon='application_form.png', children_classes=[WebForm], permissions=[PERMISSION_SOURCES_SETUP_VIEW], children_view_regex=[r'setup_web_form', r'setup_staging_folder', r'setup_source_', r'setup_pop3', r'setup_imap'])
setup_web_form_list = Link(text=_(u'web forms'), view='setup_web_form_list', sprite='application_form', icon='application_form.png', children_classes=[WebForm], permissions=[PERMISSION_SOURCES_SETUP_VIEW])
setup_staging_folder_list = Link(text=_(u'staging folders'), view='setup_staging_folder_list', sprite='folder_camera', children_classes=[StagingFolder], permissions=[PERMISSION_SOURCES_SETUP_VIEW])
setup_watch_folder_list = Link(text=_(u'watch folders'), view='setup_watch_folder_list', sprite='folder_magnify', children_classes=[WatchFolder], permissions=[PERMISSION_SOURCES_SETUP_VIEW])
setup_pop3_email_list = Link(text=_(u'POP3 email'), view='setup_pop3_email_list', sprite='email', children_classes=[POP3Email], permissions=[PERMISSION_SOURCES_SETUP_VIEW])
setup_imap_email_list = Link(text=_(u'IMAP email'), view='setup_imap_email_list', sprite='email', children_classes=[IMAPEmail], permissions=[PERMISSION_SOURCES_SETUP_VIEW])

setup_source_edit = Link(text=_(u'edit'), view='setup_source_edit', args=['source.source_type', 'source.pk'], sprite='application_form_edit', permissions=[PERMISSION_SOURCES_SETUP_EDIT])
setup_source_delete = Link(text=_(u'delete'), view='setup_source_delete', args=['source.source_type', 'source.pk'], sprite='application_form_delete', permissions=[PERMISSION_SOURCES_SETUP_DELETE])
setup_source_create = Link(text=_(u'add new source'), view='setup_source_create', args='source_type', sprite='application_form_add', permissions=[PERMISSION_SOURCES_SETUP_CREATE])
setup_source_log_list = Link(text=_(u'logs'), view='setup_source_log_list', args=['source.source_type', 'source.pk'], sprite='book', permissions=[PERMISSION_SOURCES_SETUP_EDIT])

setup_source_transformation_list = Link(text=_(u'transformations'), view='setup_source_transformation_list', args=['source.source_type', 'source.pk'], sprite='shape_move_front', permissions=[PERMISSION_SOURCES_SETUP_EDIT])
setup_source_transformation_create = Link(text=_(u'add transformation'), view='setup_source_transformation_create', args=['source.source_type', 'source.pk'], sprite='shape_square_add', permissions=[PERMISSION_SOURCES_SETUP_EDIT])
setup_source_transformation_edit = Link(text=_(u'edit'), view='setup_source_transformation_edit', args='transformation.pk', sprite='shape_square_edit', permissions=[PERMISSION_SOURCES_SETUP_EDIT])
setup_source_transformation_delete = Link(text=_(u'delete'), view='setup_source_transformation_delete', args='transformation.pk', sprite='shape_square_delete', permissions=[PERMISSION_SOURCES_SETUP_EDIT])

source_list = Link(text=_(u'Document sources'), view='setup_web_form_list', sprite='page_add', children_url_regex=[r'sources/setup'], permissions=[PERMISSION_SOURCES_SETUP_VIEW])

upload_version = Link(text=_(u'upload new version'), view='upload_version', args='object.pk', sprite='page_add', permissions=[PERMISSION_DOCUMENT_NEW_VERSION])
