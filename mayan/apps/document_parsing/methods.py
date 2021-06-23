from datetime import timedelta

from django.utils.timezone import now

from mayan.apps.common.settings import settings_db_sync_task_delay

from .events import event_parsing_document_file_submitted
from .tasks import task_parse_document_file


def method_document_parsing_submit(self, _user=None):
    latest_file = self.file_latest
    # Don't error out if document has no file.
    if latest_file:
        latest_file.submit_for_parsing(_user=_user)


def method_document_file_parsing_submit(self, _user=None):
    event_parsing_document_file_submitted.commit(
        action_object=self.document, actor=_user, target=self
    )

    if _user:
        user_id = _user.pk
    else:
        user_id = None

    task_parse_document_file.apply_async(
        eta=now() + timedelta(seconds=settings_db_sync_task_delay.value),
        kwargs={'document_file_pk': self.pk, 'user_id': user_id}
    )
