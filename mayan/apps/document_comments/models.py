from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from documents.models import Document


@python_2_unicode_compatible
class Comment(models.Model):
    document = models.ForeignKey(
        Document, db_index=True, related_name='comments',
        verbose_name=_('Document')
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, editable=False, related_name='comments',
        verbose_name=_('User'),
    )
    # Translators: Comment here is a noun and refers to the actual text stored
    comment = models.TextField(verbose_name=_('Comment'))
    submit_date = models.DateTimeField(
        auto_now_add=True, db_index=True,
        verbose_name=_('Date time submitted')
    )

    def __str__(self):
        return self.comment

    class Meta:
        get_latest_by = 'submit_date'
        ordering = ('-submit_date',)
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')
