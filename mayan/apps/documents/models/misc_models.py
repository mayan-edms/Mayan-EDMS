import logging

from django.conf import settings
from django.db import models
from django.utils.encoding import force_text, python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from ..managers import (
    DuplicatedDocumentManager, FavoriteDocumentManager, RecentDocumentManager,
    TrashCanManager
)

from .document_models import Document

__all__ = (
    'DeletedDocument', 'DuplicatedDocument', 'FavoriteDocument',
    'RecentDocument'
)
logger = logging.getLogger(name=__name__)


class DeletedDocument(Document):
    objects = TrashCanManager()

    class Meta:
        proxy = True


@python_2_unicode_compatible
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
        return force_text(self.document)


@python_2_unicode_compatible
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
        return force_text(self.document)

    def natural_key(self):
        return (self.document.natural_key(), self.user.natural_key())
    natural_key.dependencies = ['documents.Document', settings.AUTH_USER_MODEL]


@python_2_unicode_compatible
class RecentDocument(models.Model):
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

    objects = RecentDocumentManager()

    class Meta:
        ordering = ('-datetime_accessed',)
        verbose_name = _('Recent document')
        verbose_name_plural = _('Recent documents')

    def __str__(self):
        return force_text(self.document)

    def natural_key(self):
        return (self.datetime_accessed, self.document.natural_key(), self.user.natural_key())
    natural_key.dependencies = ['documents.Document', settings.AUTH_USER_MODEL]
