from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from kombu import Exchange, Queue

from common import (
    MayanAppConfig, MissingItem, menu_front_page, menu_object, menu_secondary,
    menu_sidebar, menu_setup
)
from common.signals import post_initial_setup, post_upgrade
from converter.links import link_transformation_list
from documents.models import Document
from documents.signals import post_version_upload
from mayan.celery import app
from navigation import SourceColumn
from rest_api.classes import APIEndPoint

from .classes import StagingFile
from .handlers import (
    copy_transformations_to_version, create_default_document_source,
    initialize_periodic_tasks
)
from .links import (
    link_document_create_multiple, link_document_create_siblings,
    link_setup_sources, link_setup_source_create_imap_email,
    link_setup_source_create_pop3_email,
    link_setup_source_create_watch_folder, link_setup_source_create_webform,
    link_setup_source_create_staging_folder, link_setup_source_delete,
    link_setup_source_edit, link_setup_source_logs, link_staging_file_delete,
    link_upload_version
)
from .models import (
    POP3Email, IMAPEmail, Source, SourceLog, StagingFolderSource,
    WatchFolderSource, WebFormSource
)
from .widgets import staging_file_thumbnail


class SourcesApp(MayanAppConfig):
    name = 'sources'
    test = True
    verbose_name = _('Sources')

    def ready(self):
        super(SourcesApp, self).ready()

        APIEndPoint(app=self, version_string='1')

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

        SourceColumn(
            source=StagingFile,
            label=_('Thumbnail'),
            func=lambda context: staging_file_thumbnail(
                context['object'],
                gallery_name='sources:staging_list',
                title=context['object'].filename, size='100'
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
                    'sources_periodic', Exchange('sources_periodic'),
                    routing_key='sources_periodic', delivery_mode=1
                ),
            )
        )

        app.conf.CELERY_ROUTES.update(
            {
                'sources.tasks.task_check_interval_source': {
                    'queue': 'sources_periodic'
                },
                'sources.tasks.task_source_handle_upload': {
                    'queue': 'sources'
                },
                'sources.tasks.task_upload_document': {
                    'queue': 'sources'
                },
            }
        )

        menu_front_page.bind_links(links=(link_document_create_multiple,))
        menu_object.bind_links(
            links=(link_document_create_siblings,), sources=(Document,)
        )
        menu_object.bind_links(
            links=(
                link_setup_source_edit, link_setup_source_delete,
                link_transformation_list, link_setup_source_logs
            ), sources=(
                POP3Email, IMAPEmail, StagingFolderSource, WatchFolderSource,
                WebFormSource
            )
        )
        menu_object.bind_links(
            links=(link_staging_file_delete,), sources=(StagingFile,)
        )
        menu_secondary.bind_links(
            links=(
                link_setup_sources, link_setup_source_create_webform,
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
        menu_sidebar.bind_links(
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
