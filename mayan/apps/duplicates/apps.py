from django.apps import apps
from django.db.models.signals import post_delete, post_save
from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.apps import MayanAppConfig
from mayan.apps.common.menus import menu_list_facet, menu_tools
from mayan.apps.documents.menus import menu_documents
from mayan.apps.documents.permissions import permission_document_view
from mayan.apps.documents.signals import signal_post_document_file_upload
from mayan.apps.navigation.classes import SourceColumn

from .classes import DuplicateBackend
from .handlers import (
    handler_remove_empty_duplicates_lists,
    handler_scan_duplicates_for_document,
    handler_scan_duplicates_for_document_file
)
from .links import (
    link_document_duplicate_backend_detail,
    link_document_duplicate_backend_list, link_duplicate_backend_detail,
    link_duplicate_backend_list, link_duplicate_document_scan
)


class DuplicatesApp(MayanAppConfig):
    app_namespace = 'duplicates'
    app_url = 'duplicates'
    has_rest_api = True
    has_tests = True
    name = 'mayan.apps.duplicates'
    verbose_name = _('Duplicates')

    def ready(self):
        super().ready()

        Document = apps.get_model(
            app_label='documents', model_name='Document'
        )

        DuplicateSourceDocument = self.get_model(
            model_name='DuplicateSourceDocument'
        )
        StoredDuplicateBackend = self.get_model(
            model_name='StoredDuplicateBackend'
        )
        DocumentStoredDuplicateBackend = self.get_model(
            model_name='DocumentStoredDuplicateBackend'
        )

        DuplicateBackend.load_modules()

        SourceColumn(
            attribute='__str__', include_label=True, is_identifier=True,
            label=_('Label'), source=StoredDuplicateBackend
        )
        SourceColumn(
            func=lambda context: context['object'].get_duplicated_documents(
                source_document=context.get('document', None),
                permission=permission_document_view,
                user=context['request'].user
            ).count(), include_label=True, label=_('Documents'),
            source=StoredDuplicateBackend
        )
        SourceColumn(
            func=lambda context: context['stored_backend'].get_duplicated_documents(
                source_document=context.get('document', None),
                permission=permission_document_view,
                user=context['request'].user
            ).count() - 1, include_label=True, label=_('Duplicates'),
            order=99, source=DuplicateSourceDocument
        )

        menu_documents.bind_links(
            links=(link_duplicate_backend_list,)
        )

        menu_list_facet.bind_links(
            links=(link_document_duplicate_backend_list,),
            sources=(Document,)
        )
        menu_list_facet.bind_links(
            links=(link_document_duplicate_backend_detail,),
            sources=(DocumentStoredDuplicateBackend,)
        )
        menu_list_facet.bind_links(
            links=(link_duplicate_backend_detail,),
            sources=(StoredDuplicateBackend,)
        )
        menu_list_facet.add_proxy_exclusion(
            source=DocumentStoredDuplicateBackend

        )
        menu_tools.bind_links(
            links=(link_duplicate_document_scan,)
        )

        post_delete.connect(
            dispatch_uid='duplicates_handler_remove_empty_duplicates_lists',
            receiver=handler_remove_empty_duplicates_lists,
            sender=Document
        )
        post_save.connect(
            dispatch_uid='duplicates_handler_scan_duplicates_for_document',
            receiver=handler_scan_duplicates_for_document,
            sender=Document
        )
        signal_post_document_file_upload.connect(
            dispatch_uid='duplicates_handler_scan_duplicates_for_document_file',
            receiver=handler_scan_duplicates_for_document_file
        )
