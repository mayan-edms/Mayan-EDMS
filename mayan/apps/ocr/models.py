from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from documents.models import DocumentVersion


@python_2_unicode_compatible
class DocumentVersionOCRError(models.Model):
    document_version = models.ForeignKey(DocumentVersion, verbose_name=_('Document version'))
    datetime_submitted = models.DateTimeField(verbose_name=_('Date time submitted'), auto_now=True, db_index=True)
    result = models.TextField(blank=True, null=True, verbose_name=_('Result'))

    def __str__(self):
        return unicode(self.document_version)

    class Meta:
        ordering = ('datetime_submitted',)
        verbose_name = _('Document Version OCR Error')
        verbose_name_plural = _('Document Version OCR Errors')
