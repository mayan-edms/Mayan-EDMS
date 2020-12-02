import logging

from django.conf import settings
from django.db import models
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _

from ..managers import FavoriteDocumentManager

from .document_models import Document

__all__ = ('FavoriteDocument',)
logger = logging.getLogger(name=__name__)


class FavoriteDocument(models.Model):
    """
    Keeps a list of the favorited documents of a given user
    """
    user = models.ForeignKey(
        db_index=True, editable=False, on_delete=models.CASCADE,
        to=settings.AUTH_USER_MODEL, verbose_name=_('User')
    )
    document = models.ForeignKey(
        editable=False, on_delete=models.CASCADE, related_name='favorites',
        to=Document, verbose_name=_('Document')
    )

    objects = FavoriteDocumentManager()

    class Meta:
        verbose_name = _('Favorite document')
        verbose_name_plural = _('Favorite documents')

    def __str__(self):
        return force_text(s=self.document)

    def natural_key(self):
        return (self.document.natural_key(), self.user.natural_key())
    natural_key.dependencies = ['documents.Document', settings.AUTH_USER_MODEL]
