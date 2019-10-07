from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.apps import MayanAppConfig
from mayan.apps.common.html_widgets import TwoStateWidget
from mayan.apps.common.menus import menu_tools
from mayan.apps.navigation.classes import SourceColumn

from .classes import CeleryQueue, Task
from .dependencies import *  # NOQA
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
            source=CeleryQueue, label=_('Label'), attribute='label'
        )
        SourceColumn(
            source=CeleryQueue, label=_('Name'), attribute='name'
        )
        SourceColumn(
            attribute='default_queue', label=_('Default queue?'),
            source=CeleryQueue, widget=TwoStateWidget
        )
        SourceColumn(
            attribute='transient', label=_('Is transient?'),
            source=CeleryQueue, widget=TwoStateWidget
        )
        SourceColumn(
            source=Task, label=_('Type'), attribute='task_type'
        )
        SourceColumn(
            source=Task, label=_('Start time'), attribute='get_time_started'
        )
        SourceColumn(
            source=Task, label=_('Host'),
            func=lambda context: context['object'].kwargs['hostname']
        )
        SourceColumn(
            source=Task, label=_('Arguments'),
            func=lambda context: context['object'].kwargs['args']
        )
        SourceColumn(
            source=Task, label=_('Keyword arguments'),
            func=lambda context: context['object'].kwargs['kwargs']
        )
        SourceColumn(
            source=Task, label=_('Worker process ID'),
            func=lambda context: context['object'].kwargs['worker_pid']
        )

        menu_tools.bind_links(links=(link_task_manager,))
