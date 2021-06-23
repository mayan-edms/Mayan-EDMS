from django.apps import apps
from django.utils.translation import ugettext_lazy as _

from mayan.apps.acls.classes import ModelPermission
from mayan.apps.common.apps import MayanAppConfig
from mayan.apps.common.classes import ModelQueryFields
from mayan.apps.common.menus import (
    menu_facet, menu_main, menu_multi_item, menu_secondary
)
from mayan.apps.dashboards.dashboards import dashboard_main
from mayan.apps.events.classes import ModelEventType
from mayan.apps.navigation.classes import SourceColumn

from .dashboard_widgets import DashboardWidgetTotalCheckouts
from .events import (
    event_document_auto_checked_in, event_document_checked_in,
    event_document_checked_out, event_document_forcefully_checked_in
)
from .hooks import hook_is_new_file_allowed
from .links import (
    link_check_in_document, link_check_in_document_multiple,
    link_check_out_document, link_check_out_document_multiple,
    link_check_out_info, link_check_out_list
)
from .methods import (
    method_check_in, method_get_check_out_info, method_get_check_out_state,
    method_is_checked_out
)
from .permissions import (
    permission_document_check_in, permission_document_check_in_override,
    permission_document_check_out, permission_document_check_out_detail_view
)


class CheckoutsApp(MayanAppConfig):
    app_namespace = 'checkouts'
    app_url = 'checkouts'
    has_rest_api = True
    has_tests = True
    name = 'mayan.apps.checkouts'
    verbose_name = _('Checkouts')

    def ready(self):
        super().ready()

        CheckedOutDocument = self.get_model(model_name='CheckedOutDocument')
        DocumentCheckout = self.get_model(model_name='DocumentCheckout')
        Document = apps.get_model(
            app_label='documents', model_name='Document'
        )
        DocumentFile = apps.get_model(
            app_label='documents', model_name='DocumentFile'
        )

        Document.add_to_class(name='check_in', value=method_check_in)
        Document.add_to_class(
            name='get_check_out_info', value=method_get_check_out_info
        )
        Document.add_to_class(
            name='get_check_out_state', value=method_get_check_out_state
        )
        Document.add_to_class(
            name='is_checked_out', value=method_is_checked_out
        )

        DocumentFile.register_pre_create_hook(
            func=hook_is_new_file_allowed
        )

        ModelEventType.register(
            model=Document, event_types=(
                event_document_auto_checked_in, event_document_checked_in,
                event_document_checked_out, event_document_forcefully_checked_in
            )
        )

        ModelPermission.register(
            model=Document, permissions=(
                permission_document_check_out,
                permission_document_check_in,
                permission_document_check_in_override,
                permission_document_check_out_detail_view
            )
        )
        ModelPermission.register_inheritance(
            model=DocumentCheckout, related='document'
        )

        model_query_fields_document = ModelQueryFields(model=Document)
        model_query_fields_document.add_select_related_field(field_name='documentcheckout')

        SourceColumn(
            attribute='get_user_display', include_label=True, order=99,
            source=CheckedOutDocument
        )
        SourceColumn(
            attribute='get_checkout_datetime', include_label=True, order=99,
            source=CheckedOutDocument
        )
        SourceColumn(
            attribute='get_checkout_expiration', include_label=True, order=99,
            source=CheckedOutDocument
        )

        dashboard_main.add_widget(
            widget=DashboardWidgetTotalCheckouts, order=-1
        )

        menu_facet.bind_links(
            links=(link_check_out_info,), sources=(Document,)
        )
        menu_main.bind_links(links=(link_check_out_list,), position=98)
        menu_multi_item.bind_links(
            links=(
                link_check_in_document_multiple,
            ), sources=(CheckedOutDocument,)
        )
        menu_multi_item.bind_links(
            links=(
                link_check_in_document_multiple,
                link_check_out_document_multiple,
            ), sources=(Document,)
        )
        menu_multi_item.unbind_links(
            links=(
                link_check_out_document_multiple,
            ), sources=(CheckedOutDocument,)
        )
        menu_secondary.bind_links(
            links=(link_check_out_document, link_check_in_document),
            sources=(
                'checkouts:check_out_info', 'checkouts:check_out_document',
                'checkouts:check_in_document'
            )
        )
