from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.apps import MayanAppConfig
from mayan.apps.common.classes import MissingItem
from mayan.apps.common.html_widgets import TwoStateWidget
from mayan.apps.common.menus import (
    menu_list_facet, menu_object, menu_secondary, menu_setup
)
from mayan.apps.common.signals import post_initial_setup, post_upgrade
from mayan.apps.converter.links import link_transformation_list
from mayan.apps.documents.menus import menu_documents
from mayan.apps.documents.signals import post_version_upload
from mayan.apps.navigation.classes import SourceColumn

from .classes import StagingFile
from .dependencies import *  # NOQA
from .handlers import (
    handler_copy_transformations_to_version,
    handler_create_default_document_source, handler_initialize_periodic_tasks
)
from .links import (
    link_document_create_multiple, link_setup_sources,
    link_setup_source_check_now, link_setup_source_create_imap_email,
    link_setup_source_create_pop3_email, link_setup_source_create_sane_scanner,
    link_setup_source_create_watch_folder, link_setup_source_create_webform,
    link_setup_source_create_staging_folder, link_setup_source_delete,
    link_setup_source_edit, link_setup_source_logs, link_staging_file_delete,
    link_document_version_upload
)
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

        POP3Email = self.get_model(model_name='POP3Email')
        IMAPEmail = self.get_model(model_name='IMAPEmail')
        Source = self.get_model(model_name='Source')
        SourceLog = self.get_model(model_name='SourceLog')
        SaneScanner = self.get_model(model_name='SaneScanner')
        StagingFolderSource = self.get_model(model_name='StagingFolderSource')
        WatchFolderSource = self.get_model(model_name='WatchFolderSource')
        WebFormSource = self.get_model(model_name='WebFormSource')

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
            attribute='label', is_identifier=True, is_sortable=True,
            source=Source
        )
        SourceColumn(
            attribute='class_fullname', label=_('Type'), source=Source
        )
        SourceColumn(
            attribute='enabled', is_sortable=True, source=Source,
            widget=TwoStateWidget
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
            links=(link_document_version_upload,),
            sources=(
                'documents:document_version_list', 'documents:upload_version',
                'documents:document_version_revert'
            )
        )

        post_upgrade.connect(
            receiver=handler_initialize_periodic_tasks,
            dispatch_uid='sources_handler_initialize_periodic_tasks'
        )
        post_initial_setup.connect(
            receiver=handler_create_default_document_source,
            dispatch_uid='sources_handler_create_default_document_source'
        )
        post_version_upload.connect(
            receiver=handler_copy_transformations_to_version,
            dispatch_uid='sources_handler_copy_transformations_to_version'
        )
