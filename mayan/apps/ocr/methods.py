from datetime import timedelta

from django.utils.timezone import now

from mayan.apps.common.settings import settings_db_sync_task_delay

from .events import event_ocr_document_file_submit
from .tasks import task_document_file_process


def method_document_ocr_submit(self):
    latest_file = self.latest_file
    # Don't error out if document has no file
    if latest_file:
        latest_file.submit_for_ocr()


def method_document_file_ocr_submit(self):
    event_ocr_document_file_submit.commit(
        action_object=self.document, target=self
    )

    task_document_file_process.apply_async(
        eta=now() + timedelta(seconds=settings_db_sync_task_delay.value),
        kwargs={'document_file_pk': self.pk}
    )
