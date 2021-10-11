from django.utils.translation import ugettext_lazy as _

from mayan.apps.documents.models.document_version_models import DocumentVersion

from ..permissions import (
    permission_send_document_version_attachment,
    permission_send_document_version_link
)

from .base import ObjectAttachmentMailView, ObjectLinkMailView


class MailDocumentVersionAttachmentView(ObjectAttachmentMailView):
    object_permission = permission_send_document_version_attachment
    pk_url_kwarg = 'document_version_id'
    source_queryset = DocumentVersion.valid.all()
    success_message = _(
        '%(count)d document version queued for email delivery'
    )
    success_message_plural = _(
        '%(count)d document versions queued for email delivery'
    )
    title = 'Email document version'
    title_plural = 'Email documents version'
    title_document = 'Email document version: %s'


class MailDocumentVersionLinkView(ObjectLinkMailView):
    object_permission = permission_send_document_version_link
    pk_url_kwarg = 'document_version_id'
    source_queryset = DocumentVersion.valid.all()
    success_message = _(
        '%(count)d document version link queued for email delivery'
    )
    success_message_plural = _(
        '%(count)d document version links queued for email delivery'
    )
    title = 'Email document version link'
    title_plural = 'Email document version links'
    title_document = 'Email link for document version: %s'
