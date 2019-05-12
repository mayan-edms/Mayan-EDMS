from __future__ import absolute_import, unicode_literals

from django.apps import apps
from django.db.models.signals import pre_save
from django.utils.translation import ugettext_lazy as _

from mayan.apps.acls.classes import ModelPermission
from mayan.apps.common.apps import MayanAppConfig
from mayan.apps.common.menus import menu_facet, menu_main, menu_secondary
from mayan.apps.dashboards.dashboards import dashboard_main
from mayan.apps.events.classes import ModelEventType

from .dashboard_widgets import DashboardWidgetTotalCheckouts
from .events import (
    event_document_auto_check_in, event_document_check_in,
    event_document_check_out, event_document_forceful_check_in
)
from .handlers import handler_check_new_version_creation
from .links import (
    link_check_in_document, link_check_out_document, link_check_out_info,
    link_check_out_list
)
from .methods import (
    method_check_in, method_get_check_out_info, method_get_check_out_state,
    method_is_checked_out
)
from .permissions import (
    permission_document_check_in, permission_document_check_in_override,
    permission_document_check_out, permission_document_check_out_detail_view
)
from .tasks import task_check_expired_check_outs  # NOQA
# This import is required so that celerybeat can find the task


class CheckoutsApp(MayanAppConfig):
    app_namespace = 'checkouts'
    app_url = 'checkouts'
    has_rest_api = True
    has_tests = True
    name = 'mayan.apps.checkouts'
    verbose_name = _('Checkouts')

    def ready(self):
        super(CheckoutsApp, self).ready()

        Document = apps.get_model(
            app_label='documents', model_name='Document'
        )
        DocumentVersion = apps.get_model(
            app_label='documents', model_name='DocumentVersion'
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

        ModelEventType.register(
            model=Document, event_types=(
                event_document_auto_check_in, event_document_check_in,
                event_document_check_out, event_document_forceful_check_in
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

        dashboard_main.add_widget(
            widget=DashboardWidgetTotalCheckouts, order=-1
        )

        menu_facet.bind_links(
            links=(link_check_out_info,), sources=(Document,)
        )
        menu_main.bind_links(links=(link_check_out_list,), position=98)
        menu_secondary.bind_links(
            links=(link_check_out_document, link_check_in_document),
            sources=(
                'checkouts:check_out_info', 'checkouts:check_out_document',
                'checkouts:check_in_document'
            )
        )

        pre_save.connect(
            dispatch_uid='checkouts_handler_check_new_version_creation',
            receiver=handler_check_new_version_creation,
            sender=DocumentVersion
        )
