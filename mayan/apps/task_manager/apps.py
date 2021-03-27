import logging

from kombu import Connection

from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.apps import MayanAppConfig
from mayan.apps.common.menus import menu_tools
from mayan.apps.navigation.classes import SourceColumn
from mayan.apps.views.html_widgets import TwoStateWidget

from .classes import CeleryQueue, Task
from .links import link_task_manager
from .settings import (
    setting_celery_broker_login_method, setting_celery_broker_url,
    setting_celery_broker_use_ssl
)

logger = logging.getLogger(name=__name__)


class TaskManagerApp(MayanAppConfig):
    app_namespace = 'task_manager'
    app_url = 'task_manager'
    name = 'mayan.apps.task_manager'
    verbose_name = _('Task manager')

    def check_connectivity(self):
        celery_broker_url = setting_celery_broker_url.value

        try:
            connection = Connection(
                celery_broker_url, connect_timeout=0.1,
                login_method=setting_celery_broker_login_method.value,
                ssl=setting_celery_broker_use_ssl.value
            )
            connection.ensure_connection(
                interval_step=0, interval_max=0, interval_start=0, timeout=0.1
            )
        except Exception as exception:
            raise RuntimeError(
                'Failed to connect to the Celery broker instance at {}; {}'.format(
                    celery_broker_url, exception
                )
            ) from exception
        else:
            connection.release()

    def ready(self):
        super(TaskManagerApp, self).ready()

        self.check_connectivity()

        CeleryQueue.load_modules()

        SourceColumn(
            attribute='label', is_identifier=True, label=_('Label'),
            source=CeleryQueue
        )
        SourceColumn(
            attribute='name', include_label=True, label=_('Name'),
            source=CeleryQueue
        )
        SourceColumn(
            attribute='default_queue', include_label=True,
            label=_('Default queue?'), source=CeleryQueue,
            widget=TwoStateWidget
        )
        SourceColumn(
            attribute='transient', include_label=True,
            label=_('Is transient?'), source=CeleryQueue,
            widget=TwoStateWidget
        )
        SourceColumn(
            attribute='task_type', include_label=True, label=_('Type'),
            source=Task
        )
        SourceColumn(
            attribute='get_time_started', include_label=True,
            label=_('Start time'), source=Task
        )
        SourceColumn(
            func=lambda context: context['object'].kwargs['hostname'],
            include_label=True, label=_('Host'), source=Task
        )
        SourceColumn(
            func=lambda context: context['object'].kwargs['args'],
            include_label=True, label=_('Arguments'), source=Task
        )
        SourceColumn(
            func=lambda context: context['object'].kwargs['kwargs'],
            include_label=True, label=_('Keyword arguments'), source=Task
        )
        SourceColumn(
            func=lambda context: context['object'].kwargs['worker_pid'],
            include_label=True, label=_('Worker process ID'), source=Task
        )

        menu_tools.bind_links(links=(link_task_manager,))
