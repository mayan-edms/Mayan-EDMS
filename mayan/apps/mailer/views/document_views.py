from django.utils.translation import ugettext_lazy as _

from mayan.apps.documents.models import Document

from ..permissions import permission_send_document_link

from .base import ObjectLinkMailView


class MailDocumentLinkView(ObjectLinkMailView):
    object_permission = permission_send_document_link
    pk_url_kwarg = 'document_id'
    source_queryset = Document.valid.all()
    success_message = _('%(count)d document link queued for email delivery')
    success_message_plural = _(
        '%(count)d document links queued for email delivery'
    )
    title = 'Email document link'
    title_plural = 'Email document links'
    title_document = 'Email link for document: %s'
