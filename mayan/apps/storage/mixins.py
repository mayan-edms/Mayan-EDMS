from django.core.files.base import ContentFile
from django.db import models
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _, ugettext

from mayan.apps.acls.models import AccessControlList
from mayan.apps.permissions.models import StoredPermission


class ModelMixinDatabaseFile(models.Model):
    filename = models.CharField(
        db_index=True, max_length=255, verbose_name=_('Filename')
    )
    datetime = models.DateTimeField(
        auto_now_add=True, verbose_name=_('Date time')
    )

    def delete(self, *args, **kwargs):
        if self.file.name:
            self.file.storage.delete(name=self.file.name)
        return super().delete(*args, **kwargs)

    def open(self, mode=None):
        return self.file.storage.open(
            mode=mode or self.file.file.mode, name=self.file.name
        )

    def save(self, *args, **kwargs):
        if not self.file:
            self.file = ContentFile(
                content='', name=self.filename or ugettext('Unnamed file')
            )

        self.filename = self.filename or force_text(s=self.file)
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


class ViewMixinRelatedObjectPermission:
    def get_source_queryset(self):
        queryset = super().get_source_queryset()
        permission_values = queryset.values('permission')
        stored_permission_queryset = StoredPermission.objects.filter(
            pk__in=permission_values
        )

        result = queryset.none()
        for stored_permission in stored_permission_queryset:
            result = result | AccessControlList.objects.restrict_queryset(
                permission=stored_permission.volatile_permission,
                queryset=queryset, user=self.request.user
            )

        result = result | queryset.filter(permission__isnull=True)
        return result.distinct()
