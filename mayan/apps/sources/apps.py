from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from kombu import Exchange, Queue

from mayan.apps.common.apps import MayanAppConfig
from mayan.apps.common.classes import MissingItem
from mayan.apps.common.menus import (
    menu_list_facet, menu_object, menu_secondary, menu_setup
)
from mayan.apps.common.signals import post_initial_setup, post_upgrade
from mayan.apps.converter.links import link_transformation_list
from mayan.apps.documents.menus import menu_documents
from mayan.apps.documents.signals import post_version_upload
from mayan.apps.navigation import SourceColumn
from mayan.celery import app

from .classes import StagingFile
from .handlers import (
    copy_transformations_to_version, create_default_document_source,
    initialize_periodic_tasks
)
from .links import (
    link_document_create_multiple, link_setup_sources,
    link_setup_source_check_now, link_setup_source_create_imap_email,
    link_setup_source_create_pop3_email, link_setup_source_create_sane_scanner,
    link_setup_source_create_watch_folder, link_setup_source_create_webform,
    link_setup_source_create_staging_folder, link_setup_source_delete,
    link_setup_source_edit, link_setup_source_logs, link_staging_file_delete,
    link_upload_version
)
from .queues import *  # NOQA
from .widgets import StagingFileThumbnailWidget


class SourcesApp(MayanAppConfig):
    app_namespace = 'sources'
    app_url = 'sources'
    has_rest_api = True
    has_tests = True
    name = 'mayan.apps.sources'
    verbose_name = _('Sources')

    def ready(self):
        super(SourcesApp, self).ready()

        POP3Email = self.get_model('POP3Email')
        IMAPEmail = self.get_model('IMAPEmail')
        Source = self.get_model('Source')
        SourceLog = self.get_model('SourceLog')
        SaneScanner = self.get_model('SaneScanner')
        StagingFolderSource = self.get_model('StagingFolderSource')
        WatchFolderSource = self.get_model('WatchFolderSource')
        WebFormSource = self.get_model('WebFormSource')

        MissingItem(
            label=_('Create a document source'),
            description=_(
                'Document sources are the way in which new documents are '
                'feed to Mayan EDMS, create at least a web form source to '
                'be able to upload documents from a browser.'
            ),
            condition=lambda: not Source.objects.exists(),
            view='sources:setup_source_list'
        )

        SourceColumn(
            source=StagingFile,
            label=_('Created'),
            func=lambda context: context['object'].get_date_time_created()
        )

        html_widget = StagingFileThumbnailWidget()
        SourceColumn(
            source=StagingFile,
            label=_('Thumbnail'),
            func=lambda context: html_widget.render(
                instance=context['object'],
            )
        )

        SourceColumn(
            source=SourceLog,
            label=_('Date time'),
            func=lambda context: context['object'].datetime
        )
        SourceColumn(
            source=SourceLog,
            label=_('Message'),
            func=lambda context: context['object'].message
        )

        app.conf.CELERY_QUEUES.extend(
            (
                Queue(
                    'sources', Exchange('sources'), routing_key='sources'
                ),
                Queue(
                    'sources_fast', Exchange('sources_fast'),
                    routing_key='sources_fast', delivery_mode=1
                ),
                Queue(
                    'sources_periodic', Exchange('sources_periodic'),
                    routing_key='sources_periodic', delivery_mode=1
                ),
            )
        )

        app.conf.CELERY_ROUTES.update(
            {
                'mayan.apps.sources.tasks.task_check_interval_source': {
                    'queue': 'sources_periodic'
                },
                'mayan.apps.sources.tasks.task_generate_staging_file_image': {
                    'queue': 'sources_fast'
                },
                'mayan.apps.sources.tasks.task_source_handle_upload': {
                    'queue': 'sources'
                },
                'mayan.apps.sources.tasks.task_upload_document': {
                    'queue': 'sources'
                },
            }
        )
        menu_documents.bind_links(links=(link_document_create_multiple,))

        menu_list_facet.bind_links(
            links=(
                link_setup_source_logs, link_transformation_list,
            ), sources=(
                POP3Email, IMAPEmail, SaneScanner, StagingFolderSource,
                WatchFolderSource, WebFormSource
            )
        )

        menu_object.bind_links(
            links=(
                link_setup_source_delete, link_setup_source_edit
            ), sources=(
                POP3Email, IMAPEmail, SaneScanner, StagingFolderSource,
                WatchFolderSource, WebFormSource
            )
        )
        menu_object.bind_links(
            links=(link_staging_file_delete,), sources=(StagingFile,)
        )
        menu_object.bind_links(
            links=(link_setup_source_check_now,),
            sources=(IMAPEmail, POP3Email, WatchFolderSource,)
        )
        menu_secondary.bind_links(
            links=(
                link_setup_sources, link_setup_source_create_webform,
                link_setup_source_create_sane_scanner,
                link_setup_source_create_staging_folder,
                link_setup_source_create_pop3_email,
                link_setup_source_create_imap_email,
                link_setup_source_create_watch_folder
            ), sources=(
                POP3Email, IMAPEmail, StagingFolderSource, WatchFolderSource,
                WebFormSource, 'sources:setup_source_list',
                'sources:setup_source_create'
            )
        )
        menu_setup.bind_links(links=(link_setup_sources,))
        menu_secondary.bind_links(
            links=(link_upload_version,),
            sources=(
                'documents:document_version_list', 'documents:upload_version',
                'documents:document_version_revert'
            )
        )

        post_upgrade.connect(
            initialize_periodic_tasks,
            dispatch_uid='initialize_periodic_tasks'
        )
        post_initial_setup.connect(
            create_default_document_source,
            dispatch_uid='create_default_document_source'
        )
        post_version_upload.connect(
            copy_transformations_to_version,
            dispatch_uid='copy_transformations_to_version'
        )
