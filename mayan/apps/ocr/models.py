from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import force_text, python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from documents.models import DocumentPage, DocumentType, DocumentVersion

from .managers import DocumentPageOCRContentManager


class DocumentTypeSettings(models.Model):
    """
    Define for OCR for a specific document should behave
    """
    document_type = models.OneToOneField(
        on_delete=models.CASCADE, related_name='ocr_settings',
        to=DocumentType, unique=True, verbose_name=_('Document type')
    )
    auto_ocr = models.BooleanField(
        default=True,
        verbose_name=_('Automatically queue newly created documents for OCR.')
    )

    class Meta:
        verbose_name = _('Document type settings')
        verbose_name_plural = _('Document types settings')


@python_2_unicode_compatible
class DocumentPageOCRContent(models.Model):
    document_page = models.OneToOneField(
        on_delete=models.CASCADE, related_name='ocr_content',
        to=DocumentPage, verbose_name=_('Document page')
    )
    content = models.TextField(blank=True, verbose_name=_('Content'))

    objects = DocumentPageOCRContentManager()

    class Meta:
        verbose_name = _('Document page OCR content')
        verbose_name_plural = _('Document pages OCR contents')

    def __str__(self):
        return force_text(self.document_page)


@python_2_unicode_compatible
class DocumentVersionOCRError(models.Model):
    document_version = models.ForeignKey(
        on_delete=models.CASCADE, related_name='ocr_errors',
        to=DocumentVersion, verbose_name=_('Document version')
    )
    datetime_submitted = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name=_('Date time submitted')
    )
    result = models.TextField(blank=True, null=True, verbose_name=_('Result'))

    class Meta:
        ordering = ('datetime_submitted',)
        verbose_name = _('Document version OCR error')
        verbose_name_plural = _('Document version OCR errors')

    def __str__(self):
        return force_text(self.document_version)
