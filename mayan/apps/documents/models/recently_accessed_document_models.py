import logging

from django.conf import settings
from django.db import models
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _

from ..managers import RecentlyAccessedDocumentManager

from .document_models import Document

__all__ = ('RecentlyAccessedDocument',)
logger = logging.getLogger(name=__name__)


class RecentlyAccessedDocument(models.Model):
    """
    Keeps a list of the n most recent accessed or created document for
    a given user
    """
    user = models.ForeignKey(
        db_index=True, editable=False, on_delete=models.CASCADE,
        to=settings.AUTH_USER_MODEL, verbose_name=_('User')
    )
    document = models.ForeignKey(
        editable=False, on_delete=models.CASCADE, related_name='recent',
        to=Document, verbose_name=_('Document')
    )
    datetime_accessed = models.DateTimeField(
        auto_now=True, db_index=True, verbose_name=_('Accessed')
    )

    objects = RecentlyAccessedDocumentManager()

    class Meta:
        ordering = ('-datetime_accessed',)
        verbose_name = _('Recent document')
        verbose_name_plural = _('Recent documents')

    def __str__(self):
        return force_text(s=self.document)

    def natural_key(self):
        return (self.datetime_accessed, self.document.natural_key(), self.user.natural_key())
    natural_key.dependencies = ['documents.Document', settings.AUTH_USER_MODEL]
