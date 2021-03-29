from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.apps import MayanAppConfig
from mayan.apps.common.menus import menu_secondary
from mayan.apps.navigation.classes import SourceColumn

from .links import link_object_error_list_clear
from .mixins import LoggingAppConfigMixin


class LoggingApp(LoggingAppConfigMixin, MayanAppConfig):
    app_namespace = 'logging'
    app_url = 'logging'
    has_tests = True
    name = 'mayan.apps.logging'
    verbose_name = _('Logging')

    def ready(self, *args, **kwargs):
        super().ready(*args, **kwargs)

        ErrorLogPartitionEntry = self.get_model(
            model_name='ErrorLogPartitionEntry'
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
