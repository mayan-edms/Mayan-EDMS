from django.apps import apps
from django.db.models.signals import pre_delete
from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.apps import MayanAppConfig
from mayan.apps.common.classes import MissingItem
from mayan.apps.common.signals import signal_post_initial_setup, signal_post_upgrade
from mayan.apps.converter.links import link_transformation_list
from mayan.apps.documents.menus import menu_documents
from mayan.apps.documents.signals import signal_post_version_upload
from mayan.apps.logging.classes import ErrorLog
from mayan.apps.navigation.classes import SourceColumn
from mayan.apps.views.html_widgets import TwoStateWidget
from mayan.apps.common.menus import (
    menu_list_facet, menu_object, menu_secondary, menu_setup
)

from .classes import StagingFile
from .handlers import (
    handler_copy_transformations_to_version,
    handler_create_default_document_source,
    handler_delete_interval_source_periodic_task,
    handler_initialize_periodic_tasks
)
from .links import (
    link_document_create_multiple, link_setup_sources,
    link_setup_source_check_now, link_setup_source_create_imap_email,
    link_setup_source_create_pop3_email, link_setup_source_create_sane_scanner,
    link_setup_source_create_watch_folder, link_setup_source_create_webform,
    link_setup_source_create_staging_folder, link_setup_source_delete,
    link_setup_source_edit, link_staging_file_delete,
    link_document_version_upload
)
from .widgets import StagingFileThumbnailWidget


class SourcesApp(MayanAppConfig):
    app_namespace = 'sources'
    app_url = 'sources'
    has_rest_api = True
    has_static_media = True
    has_tests = True
    name = 'mayan.apps.sources'
    static_media_ignore_patterns = (
        'sources/node_modules/dropzone/index.js',
        'sources/node_modules/dropzone/component.json'
    )
    verbose_name = _('Sources')

    def ready(self):
        super(SourcesApp, self).ready()
        DocumentType = apps.get_model(
            app_label='documents', model_name='DocumentType'
        )

        IMAPEmail = self.get_model(model_name='IMAPEmail')
        POP3Email = self.get_model(model_name='POP3Email')
        Source = self.get_model(model_name='Source')
        SaneScanner = self.get_model(model_name='SaneScanner')
        StagingFolderSource = self.get_model(model_name='StagingFolderSource')
        WatchFolderSource = self.get_model(model_name='WatchFolderSource')
        WebFormSource = self.get_model(model_name='WebFormSource')

        error_log = ErrorLog(app_config=self)
        error_log.register_model(model=IMAPEmail)
        error_log.register_model(model=POP3Email)
        error_log.register_model(model=SaneScanner)
        error_log.register_model(model=WatchFolderSource)

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
            attribute='class_fullname', include_label=True, label=_('Type'),
            source=Source
        )
        SourceColumn(
            attribute='enabled', include_label=True, is_sortable=True,
            source=Source,
            widget=TwoStateWidget
        )

        SourceColumn(
            func=lambda context: context['object'].get_date_time_created(),
            label=_('Created'), source=StagingFile,
        )

        html_widget = StagingFileThumbnailWidget()
        SourceColumn(
            source=StagingFile,
            label=_('Thumbnail'),
            func=lambda context: html_widget.render(
                instance=context['object'],
            )
        )

        menu_documents.bind_links(links=(link_document_create_multiple,))

        menu_list_facet.bind_links(
            links=(
                link_transformation_list,
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
                'documents:document_version_list',
                'documents:document_version_revert',
                'sources:document_version_upload'
            )
        )

        pre_delete.connect(
            receiver=handler_delete_interval_source_periodic_task,
            sender=DocumentType,
            dispatch_uid='sources_handler_delete_interval_source_periodic_task'
        )
        signal_post_initial_setup.connect(
            receiver=handler_create_default_document_source,
            dispatch_uid='sources_handler_create_default_document_source'
        )
        signal_post_upgrade.connect(
            receiver=handler_initialize_periodic_tasks,
            dispatch_uid='sources_handler_initialize_periodic_tasks'
        )
        signal_post_version_upload.connect(
            receiver=handler_copy_transformations_to_version,
            dispatch_uid='sources_handler_copy_transformations_to_version'
        )
