from django.apps import apps
from django.db.models.signals import pre_delete
from django.utils.translation import ugettext_lazy as _

from mayan.apps.acls.classes import ModelPermission
from mayan.apps.acls.permissions import (
    permission_acl_edit, permission_acl_view
)
from mayan.apps.common.apps import MayanAppConfig
from mayan.apps.common.classes import MissingItem
from mayan.apps.common.signals import (
    signal_post_initial_setup, signal_post_upgrade
)
from mayan.apps.converter.links import link_transformation_list
from mayan.apps.documents.permissions import (
    permission_document_create, permission_document_file_new
)
from mayan.apps.documents.menus import menu_documents
from mayan.apps.events.classes import EventModelRegistry, ModelEventType
from mayan.apps.logging.classes import ErrorLog
from mayan.apps.navigation.classes import SourceColumn
from mayan.apps.views.html_widgets import TwoStateWidget
from mayan.apps.common.menus import (
    menu_list_facet, menu_object, menu_secondary, menu_setup
)

from .classes import DocumentCreateWizardStep, SourceBackend
from .events import event_source_edited
from .handlers import (
    handler_create_default_document_source,
    handler_delete_interval_source_periodic_task,
    handler_initialize_periodic_tasks
)
from .links import (
    link_document_create_multiple, link_source_test,
    link_source_backend_selection, link_source_delete, link_source_edit,
    link_source_list, link_document_file_upload
)
from .permissions import (
    permission_sources_delete, permission_sources_edit,
    permission_sources_view
)


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
        super().ready()

        DocumentCreateWizardStep.load_modules()

        DocumentType = apps.get_model(
            app_label='documents', model_name='DocumentType'
        )

        Source = self.get_model(model_name='Source')

        SourceBackend.load_modules()

        error_log = ErrorLog(app_config=self)
        error_log.register_model(model=Source)

        EventModelRegistry.register(model=Source)

        ModelEventType.register(
            model=Source, event_types=(event_source_edited,)
        )

        MissingItem(
            label=_('Create a document source'),
            description=_(
                'Document sources are the way in which new documents are '
                'feed to Mayan EDMS, create at least a web form source to '
                'be able to upload documents from a browser.'
            ),
            condition=lambda: not Source.objects.exists(),
            view='sources:source_list'
        )

        ModelPermission.register(
            model=Source, permissions=(
                permission_acl_edit, permission_acl_view,
                permission_document_create, permission_document_file_new,
                permission_sources_delete, permission_sources_edit,
                permission_sources_view
            )
        )

        SourceColumn(
            attribute='label', is_identifier=True, is_sortable=True,
            source=Source
        )
        SourceColumn(
            attribute='get_backend_label', include_label=True,
            label=_('Type'), source=Source
        )
        SourceColumn(
            attribute='enabled', include_label=True, is_sortable=True,
            source=Source,
            widget=TwoStateWidget
        )

        menu_documents.bind_links(links=(link_document_create_multiple,))

        menu_list_facet.bind_links(
            links=(
                link_transformation_list,
            ), sources=(
                Source,
            )
        )

        menu_object.bind_links(
            links=(
                link_source_delete, link_source_edit
            ), sources=(
                Source,
            )
        )

        menu_object.bind_links(
            links=(link_source_test,),
            sources=(Source,)
        )
        menu_secondary.bind_links(
            links=(
                link_source_backend_selection, link_source_list
            ), sources=(
                Source,
                'sources:source_backend_selection', 'sources:source_create',
                'sources:source_list'
            )
        )
        menu_setup.bind_links(links=(link_source_list,))
        menu_secondary.bind_links(
            links=(link_document_file_upload,),
            sources=(
                'documents:document_file_list',
                'sources:document_file_upload'
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
