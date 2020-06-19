from datetime import timedelta

from django.utils.timezone import now

from mayan.apps.common.settings import settings_db_sync_task_delay

from .events import event_ocr_document_version_submit
from .tasks import task_document_version_process


def method_document_ocr_submit(self):
    latest_version = self.latest_version
    # Don't error out if document has no version
    if latest_version:
        latest_version.submit_for_ocr()


def method_document_version_ocr_submit(self):
    event_ocr_document_version_submit.commit(
        action_object=self.document, target=self
    )

    task_document_version_process.apply_async(
        eta=now() + timedelta(seconds=settings_db_sync_task_delay.value),
        kwargs={'document_version_pk': self.pk}
    )
