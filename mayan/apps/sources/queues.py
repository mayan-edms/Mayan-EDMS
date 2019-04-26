from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from mayan.apps.task_manager.classes import CeleryQueue

queue_sources = CeleryQueue(
    label=_('Sources'), name='sources'
)
queue_sources_periodic = CeleryQueue(
    label=_('Sources periodic'), name='sources_periodic', transient=True
)
queue_sources_fast = CeleryQueue(
    label=_('Sources fast'), name='sources_fast', transient=True
)

queue_sources_fast.add_task_type(
    label=_('Generate staging file image'),
    name='mayan.apps.sources.tasks.task_generate_staging_file_image'
)
queue_sources_periodic.add_task_type(
    label=_('Check interval source'),
    name='mayan.apps.sources.tasks.task_check_interval_source'
)
queue_sources.add_task_type(
    label=_('Handle upload'),
    name='mayan.apps.sources.tasks.task_source_handle_upload'
)
queue_sources.add_task_type(
    label=_('Upload document'),
    name='mayan.apps.sources.tasks.task_upload_document'
)
