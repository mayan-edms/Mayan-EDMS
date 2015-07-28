from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from documents.models import Document


@python_2_unicode_compatible
class Folder(models.Model):
    label = models.CharField(
        db_index=True, max_length=128, verbose_name=_('Label')
    )
    user = models.ForeignKey(User, verbose_name=_('User'))
    datetime_created = models.DateTimeField(
        auto_now_add=True, verbose_name=_('Datetime created')
    )
    documents = models.ManyToManyField(
        Document, related_name='folders', verbose_name=_('Documents')
    )

    def __str__(self):
        return self.label

    def get_absolute_url(self):
        return reverse('folders:folder_view', args=[self.pk])

    class Meta:
        ordering = ('label',)
        unique_together = ('label', 'user')
        verbose_name = _('Folder')
        verbose_name_plural = _('Folders')
