from django.utils.translation import ugettext_lazy as _

from mayan.apps.task_manager.classes import CeleryQueue
from mayan.apps.task_manager.workers import worker_slow

queue_ocr = CeleryQueue(name='ocr', label=_('OCR'), worker=worker_slow)

queue_ocr.add_task_type(
    dotted_path='mayan.apps.ocr.tasks.task_document_version_finished',
    label=_('Finish document version OCR')
)
queue_ocr.add_task_type(
    dotted_path='mayan.apps.ocr.tasks.task_document_version_page_process_ocr',
    label=_('Document version page OCR')
)
queue_ocr.add_task_type(
    dotted_path='mayan.apps.ocr.tasks.task_document_version_process',
    label=_('Document version OCR')
)
