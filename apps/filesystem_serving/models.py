from django.db import models
from django.utils.translation import ugettext_lazy as _

from documents.models import Document
from document_indexing.models import DocumentIndex


class DocumentMetadataIndex(models.Model):
    document = models.ForeignKey(Document, verbose_name=_(u'document'))
    metadata_index = models.ForeignKey(DocumentIndex, verbose_name=_(u'document index'))
    filename = models.CharField(max_length=255, verbose_name=_(u'filename'))
    suffix = models.PositiveIntegerField(default=0, verbose_name=_(u'suffix'))

    def __unicode__(self):
        return unicode(self.filename)

    class Meta:
        verbose_name = _(u'document metadata index')
        verbose_name_plural = _(u'document metadata indexes')
