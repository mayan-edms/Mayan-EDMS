import logging

from django.db import models
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _

from ..managers import DuplicatedDocumentManager

from .document_models import Document

__all__ = ('DuplicatedDocument',)
logger = logging.getLogger(name=__name__)


class DuplicatedDocument(models.Model):
    document = models.ForeignKey(
        on_delete=models.CASCADE, related_name='duplicates', to=Document,
        verbose_name=_('Document')
    )
    documents = models.ManyToManyField(
        to=Document, verbose_name=_('Duplicated documents')
    )
    datetime_added = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name=_('Added')
    )

    objects = DuplicatedDocumentManager()

    class Meta:
        verbose_name = _('Duplicated document')
        verbose_name_plural = _('Duplicated documents')

    def __str__(self):
        return force_text(s=self.document)
