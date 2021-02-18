from django.utils.translation import ugettext_lazy as _

from mayan.apps.acls.classes import ModelPermission
from mayan.apps.acls.links import link_acl_list
from mayan.apps.acls.permissions import permission_acl_edit, permission_acl_view
from mayan.apps.common.apps import MayanAppConfig
from mayan.apps.common.menus import menu_list_facet, menu_object, menu_tools
from mayan.apps.events.classes import EventModelRegistry, ModelEventType
from mayan.apps.events.permissions import permission_events_view
from mayan.apps.navigation.classes import SourceColumn

from .classes import DefinedStorage
from .events import event_download_file_downloaded
from .links import (
    link_download_file_delete, link_download_file_download,
    link_download_file_list
)


class StorageApp(MayanAppConfig):
    app_namespace = 'storage'
    app_url = 'storage'
    has_tests = True
    name = 'mayan.apps.storage'
    verbose_name = _('Storage')

    def ready(self):
        super().ready()
        DefinedStorage.load_modules()

        DownloadFile = self.get_model(model_name='DownloadFile')

        EventModelRegistry.register(model=DownloadFile)

        ModelEventType.register(
            model=DownloadFile, event_types=(
                event_download_file_downloaded,
            )
        )

        ModelPermission.register(
            model=DownloadFile, permissions=(
                permission_acl_edit, permission_acl_view,
                permission_events_view
            )
        )

        SourceColumn(
            attribute='datetime', is_identifier=True, include_label=True,
            is_sortable=True,
            source=DownloadFile
        )
        SourceColumn(
            attribute='label', include_label=True, is_sortable=True,
            source=DownloadFile
        )
        SourceColumn(
            attribute='content_object', include_label=True,
            label=_('Source object'), source=DownloadFile,
            is_attribute_absolute_url=True,
        )
        SourceColumn(
            attribute='filename', include_label=True, is_sortable=True,
            source=DownloadFile
        )

        menu_list_facet.bind_links(
            links=(link_acl_list,), sources=(DownloadFile,)
        )
        menu_object.bind_links(
            links=(
                link_download_file_delete, link_download_file_download,
            ), sources=(DownloadFile,)
        )
        menu_tools.bind_links(links=(link_download_file_list,))
