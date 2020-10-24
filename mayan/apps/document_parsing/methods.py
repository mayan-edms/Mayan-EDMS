from datetime import timedelta

from django.utils.timezone import now

from mayan.apps.common.settings import settings_db_sync_task_delay

from .events import event_parsing_document_file_submit
from .tasks import task_parse_document_file


def method_document_parsing_submit(self):
    latest_file = self.file_latest
    # Don't error out if document has no file
    if latest_file:
        latest_file.submit_for_parsing()


def method_document_file_parsing_submit(self):
    event_parsing_document_file_submit.commit(
        action_object=self.document, target=self
    )

    task_parse_document_file.apply_async(
        eta=now() + timedelta(seconds=settings_db_sync_task_delay.value),
        kwargs={'document_file_pk': self.pk},
    )
