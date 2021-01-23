from django.apps import apps
from django.db.models.signals import post_delete
from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.apps import MayanAppConfig
from mayan.apps.common.menus import menu_facet, menu_tools
from mayan.apps.documents.menus import menu_documents
from mayan.apps.documents.permissions import permission_document_view
from mayan.apps.documents.signals import signal_post_document_file_upload
from mayan.apps.navigation.classes import SourceColumn

from .handlers import (
    handler_remove_empty_duplicates_lists, handler_scan_duplicates_for
)
from .links import (
    link_document_duplicates_list, link_duplicated_document_list,
    link_duplicated_document_scan
)


class DuplicatesApp(MayanAppConfig):
    app_namespace = 'duplicates'
    app_url = 'duplicates'
    has_tests = True
    name = 'mayan.apps.duplicates'
    verbose_name = _('Duplicates')

    def ready(self):
        super().ready()

        Document = apps.get_model(
            app_label='documents', model_name='Document'
        )

        DuplicatedDocument = self.get_model(model_name='DuplicatedDocument')

        SourceColumn(
            func=lambda context: DuplicatedDocument.objects.get_duplicates_of(
                document=context['object'],
                permission=permission_document_view,
                user=context['request'].user
            ).count(), include_label=True, label=_('Duplicates'),
            source=Document, views=('duplicates:duplicated_document_list',)
        )

        menu_documents.bind_links(
            links=(link_duplicated_document_list,)
        )
        menu_tools.bind_links(
            links=(link_duplicated_document_scan,)
        )
        menu_facet.bind_links(
            links=(link_document_duplicates_list,),
            sources=(Document,)
        )

        post_delete.connect(
            dispatch_uid='duplicates_handler_remove_empty_duplicates_lists',
            receiver=handler_remove_empty_duplicates_lists,
            sender=Document
        )
        signal_post_document_file_upload.connect(
            dispatch_uid='duplicates_handler_scan_duplicates_for',
            receiver=handler_scan_duplicates_for
        )
