from datetime import timedelta

from django.utils.timezone import now

from mayan.apps.common.settings import settings_db_sync_task_delay

from .events import event_ocr_document_version_submit
from .tasks import task_document_version_ocr_process


def method_document_ocr_submit(self):
    version_active = self.version_active
    # Don't error out if document has no version
    if version_active:
        version_active.submit_for_ocr()


def method_document_version_ocr_submit(self):
    event_ocr_document_version_submit.commit(
        action_object=self.document, target=self
    )

    task_document_version_ocr_process.apply_async(
        eta=now() + timedelta(seconds=settings_db_sync_task_delay.value),
        kwargs={'document_version_id': self.pk}
    )
