from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from task_manager.classes import CeleryQueue

queue_sources = CeleryQueue(
    name='sources', label=_('Sources')
)
queue_sources_periodic = CeleryQueue(
    name='sources_periodic', label=_('Sources periodic'), transient=True
)
queue_sources_fast = CeleryQueue(
    name='sources_fast', label=_('Sources fast'), transient=True
)

queue_sources_fast.add_task_type(
    name='sources.tasks.task_generate_staging_file_image',
    label=_('Generate staging file image')
)
queue_sources_periodic.add_task_type(
    name='sources.tasks.task_check_interval_source',
    label=_('Check interval source')
)
queue_sources.add_task_type(
    name='sources.tasks.task_source_handle_upload',
    label=_('Handle upload')
)
queue_sources.add_task_type(
    name='sources.tasks.task_upload_document',
    label=_('Upload document')
)
