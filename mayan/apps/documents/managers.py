from __future__ import unicode_literals

import logging

from django.apps import apps
from django.db import models

from .settings import setting_recent_count

logger = logging.getLogger(__name__)


class RecentDocumentManager(models.Manager):
    def add_document_for_user(self, user, document):
        if user.is_authenticated():
            new_recent, created = self.model.objects.get_or_create(
                user=user, document=document
            )
            if not created:
                # document already in the recent list, just save to force
                # accessed date and time update
                new_recent.save()

            recent_to_delete = self.filter(user=user).values_list('pk', flat=True)[setting_recent_count.value:]
            self.filter(pk__in=list(recent_to_delete)).delete()

    def get_for_user(self, user):
        document_model = apps.get_model('documents', 'document')

        if user.is_authenticated():
            return document_model.objects.filter(
                recentdocument__user=user
            ).order_by('-recentdocument__datetime_accessed')
        else:
            return document_model.objects.none()


class DocumentTypeManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)


class DocumentManager(models.Manager):
    def get_queryset(self):
        return TrashCanQuerySet(
            self.model, using=self._db
        ).filter(in_trash=False)

    def invalidate_cache(self):
        for document in self.model.objects.all():
            document.invalidate_cache()


class PassthroughManager(models.Manager):
    pass


class TrashCanManager(models.Manager):
    def get_queryset(self):
        return super(
            TrashCanManager, self
        ).get_queryset().filter(in_trash=True)


class TrashCanQuerySet(models.QuerySet):
    def delete(self, to_trash=True):
        for instance in self:
            instance.delete(to_trash=to_trash)
