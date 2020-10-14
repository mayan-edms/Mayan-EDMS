from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.apps import MayanAppConfig
from mayan.apps.common.menus import menu_object, menu_tools
from mayan.apps.navigation.classes import SourceColumn

from .classes import DefinedStorage
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

        menu_object.bind_links(
            links=(
                link_download_file_delete, link_download_file_download,
            ), sources=(DownloadFile,)
        )
        menu_tools.bind_links(links=(link_download_file_list,))
