from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from mayan.apps.documents.queues import queue_uploads

queue_uploads.add_task_type(
    dotted_path='mayan.apps.importer.tasks.task_upload_new_document',
    label=_('Import new document')
)
