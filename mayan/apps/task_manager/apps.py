import logging

from celery.backends.base import DisabledBackend

from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.apps import MayanAppConfig
from mayan.apps.common.menus import menu_tools
from mayan.apps.navigation.classes import SourceColumn
from mayan.apps.views.html_widgets import TwoStateWidget
from mayan.celery import app as celery_app

from .classes import CeleryQueue, Task
from .links import link_task_manager
from .literals import TEST_CELERY_RESULT_KEY, TEST_CELERY_RESULT_VALUE

logger = logging.getLogger(name=__name__)


class TaskManagerApp(MayanAppConfig):
    app_namespace = 'task_manager'
    app_url = 'task_manager'
    name = 'mayan.apps.task_manager'
    verbose_name = _('Task manager')

    def check_broker_connectivity(self):
        connection = celery_app.connection()

        logger.debug('Starting Redis broker connectivity test')
        try:
            connection.ensure_connection(
                interval_step=0, interval_max=0, interval_start=0, timeout=0.1
            )
        except Exception as exception:
            print(
                'Failed to connect to the Celery broker at {}; {}'.format(
                    connection.as_uri(), exception
                )
            )
            raise
        else:
            connection.release()

    def check_results_backend_connectivity(self):
        backend = celery_app.backend

        if not isinstance(backend, DisabledBackend):
            retry_policy = backend.retry_policy

            backend.retry_policy = {
                'max_retries': 0, 'interval_start': 0, 'interval_step': 1,
                'interval_max': 1
            }

            logger.debug('Starting Redis result backend connectivity test')
            try:
                backend.set(
                    key=TEST_CELERY_RESULT_KEY, value=TEST_CELERY_RESULT_VALUE
                )
            except Exception as exception:
                print(
                    'Failed to connect to the Celery result backend at {}; {}'.format(
                        backend.as_uri(), exception
                    )
                )
                raise
            else:
                backend.delete(key=TEST_CELERY_RESULT_KEY)
                backend.retry_policy = retry_policy

    def ready(self):
        super().ready()

        try:
            self.check_broker_connectivity()
            self.check_results_backend_connectivity()
        except Exception:
            exit(1)

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
