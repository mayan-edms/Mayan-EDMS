from django.utils.translation import ugettext_lazy as _

from .classes import DocumentVersionModification
from .tasks import (
    task_document_version_page_list_append,
    task_document_version_page_list_reset
)


class DocumentVersionModificationPagesAppend(DocumentVersionModification):
    label = _('Append all file pages')
    description = _(
        'The current pages will be deleted and then all the '
        'document file pages will be appended as pages of this '
        'document version.'
    )

    @staticmethod
    def execute(document_version, _user):
        task_document_version_page_list_append.apply_async(
            kwargs={
                'document_version_id': document_version.pk,
                'user_id': _user.pk
            }
        )


class DocumentVersionModificationPagesReset(DocumentVersionModification):
    label = _('Reset pages to latest file')
    description = _('Match all pages to that of the latest document file.')

    @staticmethod
    def execute(document_version, _user):
        task_document_version_page_list_reset.apply_async(
            kwargs={
                'document_version_id': document_version.pk,
                'user_id': _user.pk
            }
        )
