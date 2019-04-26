from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from mayan.apps.task_manager.classes import CeleryQueue

queue_checkouts_periodic = CeleryQueue(
    label=_('Checkouts periodic'), name='checkouts_periodic', transient=True
)
queue_checkouts_periodic.add_task_type(
    label=_('Check expired checkouts'),
    name='mayan.apps.task_check_expired_check_outs'
)
