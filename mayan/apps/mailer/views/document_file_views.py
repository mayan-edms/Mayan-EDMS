from django.utils.translation import ugettext_lazy as _

from mayan.apps.documents.models.document_file_models import DocumentFile

from ..permissions import (
    permission_send_document_file_attachment,
    permission_send_document_file_link
)

from .base import ObjectAttachmentMailView, ObjectLinkMailView


class MailDocumentFileAttachmentView(ObjectAttachmentMailView):
    object_permission = permission_send_document_file_attachment
    pk_url_kwarg = 'document_file_id'
    source_queryset = DocumentFile.valid.all()
    success_message = _('%(count)d document file queued for email delivery')
    success_message_plural = _(
        '%(count)d document files queued for email delivery'
    )
    title = 'Email document file'
    title_plural = 'Email document files'
    title_document = 'Email document file: %s'


class MailDocumentFileLinkView(ObjectLinkMailView):
    object_permission = permission_send_document_file_link
    pk_url_kwarg = 'document_file_id'
    source_queryset = DocumentFile.valid.all()
    success_message = _(
        '%(count)d document file link queued for email delivery'
    )
    success_message_plural = _(
        '%(count)d document file links queued for email delivery'
    )
    title = 'Email document file link'
    title_plural = 'Email document file links'
    title_document = 'Email link for document file: %s'
