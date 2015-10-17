from __future__ import absolute_import, unicode_literals

from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from acls.models import AccessControlList
from documents.models import Document
from documents.permissions import permission_document_view
from permissions import Permission

from .managers import FolderManager


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

    objects = FolderManager()

    def __str__(self):
        return self.label

    def get_absolute_url(self):
        return reverse('folders:folder_view', args=(self.pk,))

    def natural_key(self):
        return (self.label,) + self.user.natural_key()
    natural_key.dependencies = ['auth.User']

    class Meta:
        ordering = ('label',)
        unique_together = ('label', 'user')
        verbose_name = _('Folder')
        verbose_name_plural = _('Folders')

    def get_document_count(self, user):
        queryset = self.documents

        try:
            Permission.check_permissions(user, (permission_document_view,))
        except PermissionDenied:
            queryset = AccessControlList.objects.filter_by_access(
                permission_document_view, user, queryset
            )

        return queryset.count()


class DocumentFolder(Folder):
    class Meta:
        proxy = True
        verbose_name = _('Document folder')
        verbose_name_plural = _('Document folders')
