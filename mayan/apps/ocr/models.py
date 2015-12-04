from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from documents.models import DocumentPage, DocumentType, DocumentVersion


class DocumentTypeSettings(models.Model):
    """
    Define for OCR for a specific document should behave
    """
    document_type = models.OneToOneField(
        DocumentType, related_name='ocr_settings', unique=True,
        verbose_name=_('Document type')
    )
    auto_ocr = models.BooleanField(
        default=True,
        verbose_name=_('Automatically queue newly created documents for OCR.')
    )

    class Meta:
        verbose_name = _('Document type settings')
        verbose_name_plural = _('Document types settings')


@python_2_unicode_compatible
class DocumentVersionOCRError(models.Model):
    document_version = models.ForeignKey(
        DocumentVersion, verbose_name=_('Document version')
    )
    datetime_submitted = models.DateTimeField(
        auto_now=True, db_index=True, verbose_name=_('Date time submitted')
    )
    result = models.TextField(blank=True, null=True, verbose_name=_('Result'))

    def __str__(self):
        return unicode(self.document_version)

    class Meta:
        ordering = ('datetime_submitted',)
        verbose_name = _('Document Version OCR Error')
        verbose_name_plural = _('Document Version OCR Errors')


@python_2_unicode_compatible
class DocumentPageContent(models.Model):
    """
    Model that describes a document page content
    """
    document_page = models.OneToOneField(
        DocumentPage, related_name='ocr_content',
        verbose_name=_('Document page')
    )
    content = models.TextField(blank=True, verbose_name=_('Content'))

    def __str__(self):
        return unicode(self.document_page)

    class Meta:
        verbose_name = _('Document page content')
        verbose_name_plural = _('Document pages contents')
