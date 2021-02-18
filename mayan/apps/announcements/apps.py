import logging

from django.utils.translation import ugettext_lazy as _

from mayan.apps.acls.classes import ModelPermission
from mayan.apps.acls.links import link_acl_list
from mayan.apps.acls.permissions import permission_acl_edit, permission_acl_view
from mayan.apps.common.apps import MayanAppConfig
from mayan.apps.common.classes import ModelCopy
from mayan.apps.common.menus import (
    menu_list_facet, menu_multi_item, menu_object, menu_secondary, menu_setup
)
from mayan.apps.events.classes import EventModelRegistry, ModelEventType
from mayan.apps.events.permissions import permission_events_view
from mayan.apps.navigation.classes import SourceColumn
from mayan.apps.views.html_widgets import TwoStateWidget

from .events import event_announcement_edited
from .links import (
    link_announcement_create, link_announcement_multiple_delete,
    link_announcement_single_delete, link_announcement_edit, link_announcement_list
)
from .permissions import (
    permission_announcement_delete, permission_announcement_edit,
    permission_announcement_view
)

logger = logging.getLogger(name=__name__)


class AnnouncementsApp(MayanAppConfig):
    app_namespace = 'announcements'
    app_url = 'announcements'
    has_rest_api = True
    has_tests = True
    name = 'mayan.apps.announcements'
    verbose_name = _('Announcements')

    def ready(self):
        super().ready()

        Announcement = self.get_model(model_name='Announcement')

        EventModelRegistry.register(model=Announcement)

        ModelCopy(
            model=Announcement, bind_link=True, register_permission=True
        ).add_fields(
            field_names=(
                'label', 'text', 'enabled', 'start_datetime', 'end_datetime'
            ),
        )

        ModelEventType.register(
            model=Announcement, event_types=(event_announcement_edited,)
        )

        ModelPermission.register(
            model=Announcement, permissions=(
                permission_acl_edit, permission_acl_view,
                permission_events_view, permission_announcement_delete,
                permission_announcement_edit, permission_announcement_view
            )
        )
        SourceColumn(
            attribute='label', is_identifier=True, is_sortable=True,
            source=Announcement
        )
        SourceColumn(
            attribute='enabled', include_label=True, is_sortable=True,
            source=Announcement, widget=TwoStateWidget
        )
        SourceColumn(
            attribute='start_datetime', empty_value=_('None'),
            include_label=True, is_sortable=True, source=Announcement
        )
        SourceColumn(
            attribute='end_datetime', empty_value=_('None'),
            include_label=True, is_sortable=True, source=Announcement
        )

        menu_list_facet.bind_links(
            links=(link_acl_list,), sources=(Announcement,)
        )

        menu_multi_item.bind_links(
            links=(link_announcement_multiple_delete,), sources=(Announcement,)
        )
        menu_object.bind_links(
            links=(
                link_announcement_single_delete, link_announcement_edit
            ), sources=(Announcement,)
        )
        menu_secondary.bind_links(
            links=(link_announcement_create,),
            sources=(
                Announcement, 'announcements:announcement_list',
                'announcements:announcement_create'
            )
        )
        menu_setup.bind_links(
            links=(link_announcement_list,)
        )
