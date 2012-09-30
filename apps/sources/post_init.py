from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from common.utils import encapsulate
from documents.models import Document
from navigation.api import (bind_links, register_model_list_columns,
    register_sidebar_template)
from scheduler.api import LocalScheduler

#from .settings import EMAIL_PROCESSING_INTERVAL
from .links import (staging_file_delete, setup_sources,
    setup_web_form_list, setup_staging_folder_list, setup_watch_folder_list,
    setup_pop3_email_list, setup_imap_email_list, setup_source_edit,
    setup_source_delete, setup_source_create, setup_source_log_list,
    #setup_source_transformation_list, setup_source_transformation_create,
    #setup_source_transformation_edit, setup_source_transformation_delete,
    upload_version, document_create_multiple, setup_local_scanner_list,
    setup_local_scanners_refresh)
from .models import (WebForm, StagingFolder, SourceTransformation,
    WatchFolder, POP3Email, IMAPEmail, LocalScanner)
from .staging import StagingFile
from .tasks import task_fetch_pop3_emails, task_fetch_imap_emails
from .widgets import staging_file_thumbnail

bind_links([StagingFile], [staging_file_delete])
#bind_links([SourceTransformation], [setup_source_transformation_edit, setup_source_transformation_delete])
bind_links([LocalScanner, 'setup_local_scanner_list'], [setup_local_scanners_refresh], menu_name='secondary_menu')
bind_links(['setup_imap_email_list', 'setup_pop3_email_list', 'setup_web_form_list', 'setup_staging_folder_list', 'setup_watch_folder_list', 'setup_source_create', 'setup_local_scanner_list'], [setup_web_form_list, setup_staging_folder_list, setup_pop3_email_list, setup_imap_email_list, setup_local_scanner_list], menu_name='form_header')
bind_links([WebForm, StagingFolder, POP3Email, IMAPEmail, LocalScanner, 'setup_web_form_list', 'setup_staging_folder_list', 'setup_watch_folder_list', 'setup_source_create', 'setup_pop3_email_list', 'setup_imap_email_list', 'setup_local_scanner_list'], [setup_source_create], menu_name='secondary_menu')
bind_links([WebForm], [setup_web_form_list, setup_staging_folder_list, setup_pop3_email_list, setup_imap_email_list, setup_local_scanner_list], menu_name='form_header')
bind_links([WebForm], [setup_source_edit, setup_source_delete])
bind_links([StagingFolder], [setup_web_form_list, setup_staging_folder_list, setup_pop3_email_list, setup_imap_email_list, setup_local_scanner_list], menu_name='form_header')
bind_links([StagingFolder], [setup_source_edit, setup_source_delete])
bind_links([POP3Email], [setup_web_form_list, setup_staging_folder_list, setup_pop3_email_list, setup_imap_email_list, setup_local_scanner_list], menu_name='form_header')
bind_links([POP3Email], [setup_source_edit, setup_source_delete])
bind_links([POP3Email], [setup_source_log_list])
bind_links([IMAPEmail], [setup_web_form_list, setup_staging_folder_list, setup_pop3_email_list, setup_imap_email_list, setup_local_scanner_list], menu_name='form_header')
bind_links([IMAPEmail], [setup_source_edit, setup_source_delete])
bind_links([IMAPEmail], [setup_source_log_list])
bind_links([WatchFolder], [setup_web_form_list, setup_staging_folder_list, setup_watch_folder_list, setup_imap_email_list, setup_local_scanner_list], menu_name='form_header')
bind_links([WatchFolder], [setup_source_edit, setup_source_delete])
bind_links([LocalScanner], [setup_web_form_list, setup_staging_folder_list, setup_watch_folder_list, setup_imap_email_list, setup_local_scanner_list], menu_name='form_header')
bind_links([LocalScanner], [setup_source_edit, setup_source_delete])
register_sidebar_template([LocalScanner, 'setup_local_scanner_list'], 'scanner_list.html')

# Document version
bind_links(['document_version_list', 'upload_version', 'document_version_revert', 'document_version_text_compare', 'document_version_show_diff_text'], [upload_version], menu_name='sidebar')
#bind_links(['setup_source_transformation_create', 'setup_source_transformation_edit', 'setup_source_transformation_delete', 'setup_source_transformation_list'], [setup_source_transformation_create], menu_name='sidebar')
source_views = ['setup_web_form_list', 'setup_staging_folder_list', 'setup_watch_folder_list', 'setup_source_edit', 'setup_source_delete', 'setup_source_create', 'setup_source_transformation_list', 'setup_source_transformation_edit', 'setup_source_transformation_delete', 'setup_source_transformation_create']

register_model_list_columns(StagingFile, [
        {'name':_(u'thumbnail'), 'attribute':
            encapsulate(lambda x: staging_file_thumbnail(x))
        },
    ])

#sources_scheduler = LocalScheduler('sources', _(u'Document sources'))
#sources_scheduler.add_interval_job('task_fetch_pop3_emails', _(u'Connects to the POP3 email sources and fetches the attached documents.'), task_fetch_pop3_emails, seconds=EMAIL_PROCESSING_INTERVAL)
#sources_scheduler.add_interval_job('task_fetch_imap_emails', _(u'Connects to the IMAP email sources and fetches the attached documents.'), task_fetch_imap_emails, seconds=EMAIL_PROCESSING_INTERVAL)
#sources_scheduler.start()

bind_links(['document_list_recent', 'document_list', 'document_create', 'document_create_multiple', 'upload_interactive', 'staging_file_delete'], [document_create_multiple], menu_name='secondary_menu')
bind_links([Document], [document_create_multiple], menu_name='secondary_menu')
