from mayan.apps.converter.settings import setting_image_generation_timeout

from .events import event_ocr_document_version_submitted
from .literals import TASK_DOCUMENT_VERSION_PAGE_OCR_TIMEOUT
from .tasks import task_document_version_ocr_process


def method_document_ocr_submit(self, _user=None):
    version_active = self.version_active
    # Don't error out if document has no version
    if version_active:
        version_active.submit_for_ocr(_user=_user)


def method_document_version_ocr_submit(self, _user=None):
    event_ocr_document_version_submitted.commit(
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
        kwargs={
            'document_version_id': self.pk, 'user_id': user_id
        }, timeout=(
            TASK_DOCUMENT_VERSION_PAGE_OCR_TIMEOUT + setting_image_generation_timeout.value * 2
        ) * self.pages.count()
    )
