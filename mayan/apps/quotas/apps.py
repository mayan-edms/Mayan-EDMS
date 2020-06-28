from django.apps import apps
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from mayan.apps.acls.classes import ModelPermission
from mayan.apps.acls.links import link_acl_list
from mayan.apps.acls.permissions import (
    permission_acl_edit, permission_acl_view
)
from mayan.apps.common.apps import MayanAppConfig
from mayan.apps.common.classes import ModelCopy
from mayan.apps.common.menus import (
    menu_list_facet, menu_object, menu_secondary, menu_setup
)
from mayan.apps.events.classes import EventModelRegistry, ModelEventType
from mayan.apps.events.links import (
    link_events_for_object, link_object_event_types_user_subcriptions_list
)
from mayan.apps.navigation.classes import SourceColumn
from mayan.apps.views.html_widgets import TwoStateWidget

from .classes import QuotaBackend
from .events import event_quota_created, event_quota_edited
from .links import (
    link_quota_create, link_quota_delete, link_quota_edit, link_quota_list,
    link_quota_setup
)
from .permissions import (
    permission_quota_delete, permission_quota_edit, permission_quota_view
)


class QuotasApp(MayanAppConfig):
    app_namespace = 'quotas'
    app_url = 'quotas'
    has_rest_api = False
    has_tests = True
    name = 'mayan.apps.quotas'
    verbose_name = _('Quotas')

    def ready(self, *args, **kwargs):
        super(QuotasApp, self).ready(*args, **kwargs)

        Group = apps.get_model(app_label='auth', model_name='Group')
        DocumentType = apps.get_model(
            app_label='documents', model_name='DocumentType'
        )
        Quota = self.get_model(model_name='Quota')
        User = get_user_model()

        EventModelRegistry.register(model=Quota)

        QuotaBackend.load_modules()

        ModelCopy(
            model=Quota, bind_link=True, register_permission=True
        ).add_fields(
            field_names=(
                'backend_path', 'backend_data', 'enabled',
            ),
        )

        ModelEventType.register(
            event_types=(event_quota_created, event_quota_edited),
            model=Quota
        )

        ModelPermission.register(
            model=Group, permissions=(permission_quota_edit,)
        )
        ModelPermission.register(
            model=DocumentType, permissions=(permission_quota_edit,)
        )

        ModelPermission.register(
            model=Quota, permissions=(
                permission_acl_edit, permission_acl_view,
                permission_quota_delete, permission_quota_edit,
                permission_quota_view
            )
        )

        ModelPermission.register(
            model=User, permissions=(permission_quota_edit,)
        )

        SourceColumn(
            attribute='backend_label', include_label=True, is_identifier=True,
            source=Quota
        )
        SourceColumn(
            attribute='backend_filters', include_label=True, source=Quota
        )
        SourceColumn(
            attribute='backend_usage', include_label=True, source=Quota
        )
        SourceColumn(
            attribute='enabled', include_label=True, is_sortable=True,
            source=Quota, widget=TwoStateWidget
        )

        menu_list_facet.bind_links(
            links=(
                link_acl_list, link_events_for_object,
                link_object_event_types_user_subcriptions_list,
            ), sources=(Quota,)
        )

        menu_object.bind_links(
            links=(
                link_quota_edit, link_quota_delete,
            ), sources=(Quota,)
        )

        menu_secondary.bind_links(
            links=(
                link_quota_list, link_quota_create,
            ), sources=(
                Quota, 'quotas:quota_backend_selection',
                'quotas:quota_create', 'quotas:quota_list'
            )
        )

        menu_setup.bind_links(links=(link_quota_setup,))
