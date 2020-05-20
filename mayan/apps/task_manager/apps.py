from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.apps import MayanAppConfig
from mayan.apps.common.html_widgets import TwoStateWidget
from mayan.apps.common.menus import menu_tools
from mayan.apps.navigation.classes import SourceColumn

from .classes import CeleryQueue, Task
from .links import link_task_manager
from .settings import *  # NOQA


class TaskManagerApp(MayanAppConfig):
    app_namespace = 'task_manager'
    app_url = 'task_manager'
    name = 'mayan.apps.task_manager'
    verbose_name = _('Task manager')

    def ready(self):
        super(TaskManagerApp, self).ready()

        CeleryQueue.initialize()

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
