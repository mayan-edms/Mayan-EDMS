from django.utils.translation import ugettext_lazy as _

from mayan.apps.acls.classes import ModelPermission
from mayan.apps.common.apps import MayanAppConfig
from mayan.apps.common.menus import menu_secondary, menu_tools
from mayan.apps.navigation.classes import SourceColumn
from mayan.apps.views.html_widgets import ObjectLinkWidget

from .links import (
    link_global_error_log_partition_entry_list, link_object_error_list_clear
)
from .mixins import LoggingAppConfigMixin


class LoggingApp(LoggingAppConfigMixin, MayanAppConfig):
    app_namespace = 'logging'
    app_url = 'logging'
    has_tests = True
    name = 'mayan.apps.logging'
    verbose_name = _('Logging')

    def ready(self, *args, **kwargs):
        super().ready(*args, **kwargs)

        GlobalErrorLogPartitionEntry = self.get_model(
            model_name='GlobalErrorLogPartitionEntry'
        )
        ErrorLogPartition = self.get_model(
            model_name='ErrorLogPartition'
        )
        ErrorLogPartitionEntry = self.get_model(
            model_name='ErrorLogPartitionEntry'
        )

        ModelPermission.register_inheritance(
            model=ErrorLogPartitionEntry, related='error_log_partition'
        )
        ModelPermission.register_inheritance(
            model=ErrorLogPartition, related='content_object'
        )

        SourceColumn(
            attribute='error_log_partition__name', is_sortable=True,
            source=GlobalErrorLogPartitionEntry
        )
        SourceColumn(
            attribute='get_object', source=GlobalErrorLogPartitionEntry,
            widget=ObjectLinkWidget
        )
        SourceColumn(
            attribute='datetime', is_identifier=True, is_sortable=True,
            source=ErrorLogPartitionEntry
        )
        SourceColumn(
            attribute='text', include_label=True, is_sortable=True,
            source=ErrorLogPartitionEntry
        )

        menu_secondary.bind_links(
            links=(link_object_error_list_clear,), sources=(
                'logging:object_error_list',
            )
        )
        menu_tools.bind_links(
            links=(link_global_error_log_partition_entry_list,),
        )
