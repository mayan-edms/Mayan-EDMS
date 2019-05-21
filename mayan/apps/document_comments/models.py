from __future__ import unicode_literals

import logging

from django.conf import settings
from django.db import models, transaction
from django.urls import reverse
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from mayan.apps.documents.models import Document

from .events import (
    event_document_comment_created, event_document_comment_deleted,
    event_document_comment_edited
)

logger = logging.getLogger(__name__)


@python_2_unicode_compatible
class Comment(models.Model):
    """
    Model to store one comment per document per user per date & time.
    """
    document = models.ForeignKey(
        db_index=True, on_delete=models.CASCADE, related_name='comments',
        to=Document, verbose_name=_('Document')
    )
    user = models.ForeignKey(
        editable=False, on_delete=models.CASCADE, related_name='comments',
        to=settings.AUTH_USER_MODEL, verbose_name=_('User'),
    )
    # Translators: Comment here is a noun and refers to the actual text stored
    comment = models.TextField(verbose_name=_('Comment'))
    submit_date = models.DateTimeField(
        auto_now_add=True, db_index=True,
        verbose_name=_('Date time submitted')
    )

    class Meta:
        get_latest_by = 'submit_date'
        ordering = ('-submit_date',)
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')

    def __str__(self):
        return self.comment

    def delete(self, *args, **kwargs):
        _user = kwargs.pop('_user', None)
        with transaction.atomic():
            super(Comment, self).delete(*args, **kwargs)
            event_document_comment_deleted.commit(
                actor=_user, target=self.document
            )

    def get_absolute_url(self):
        return reverse(
            viewname='comments:comment_details', kwargs={'pk': self.pk}
        )

    def get_user_label(self):
        if self.user.get_full_name():
            return self.user.get_full_name()
        else:
            return self.user.username
    get_user_label.short_description = _('User')

    def save(self, *args, **kwargs):
        _user = kwargs.pop('_user', None) or self.user
        created = not self.pk

        with transaction.atomic():
            super(Comment, self).save(*args, **kwargs)
            if created:
                event_document_comment_created.commit(
                    action_object=self.document, actor=_user, target=self,
                )
            else:
                event_document_comment_edited.commit(
                    action_object=self.document, actor=_user, target=self,
                )
