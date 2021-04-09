from datetime import timedelta

from django.utils.timezone import now

from mayan.apps.common.settings import settings_db_sync_task_delay
from mayan.apps.documents.literals import DOCUMENT_IMAGE_TASK_TIMEOUT

from .events import event_ocr_document_version_submit
from .literals import TASK_DOCUMENT_VERSION_PAGE_OCR_TIMEOUT
from .tasks import task_document_version_ocr_process


def method_document_ocr_submit(self, _user=None):
    version_active = self.version_active
    # Don't error out if document has no version
    if version_active:
        version_active.submit_for_ocr(_user=_user)


def method_document_version_ocr_submit(self, _user=None):
    event_ocr_document_version_submit.commit(
        action_object=self.document, actor=_user, target=self
    )

    if _user:
        user_id = _user.pk
    else:
        user_id = None

    # Timeout calculation logic:
    # Total timeout for the document version task should be the
    # file page render timeout + the version page timeout + version page OCR
    # timeout x the total version pages. This decreases the probability of
    # the OCR task getting killed before the document file and version page
    # rendering finishes.

    task_document_version_ocr_process.apply_async(
        eta=now() + timedelta(seconds=settings_db_sync_task_delay.value),
        kwargs={
            'document_version_id': self.pk, 'user_id': user_id
        }, timeout=(
            TASK_DOCUMENT_VERSION_PAGE_OCR_TIMEOUT + DOCUMENT_IMAGE_TASK_TIMEOUT * 2
        ) * self.pages.count()
    )
