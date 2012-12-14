from __future__ import absolute_import

from ast import literal_eval
from datetime import datetime

from django.db import models

from .conf.settings import RECENT_COUNT


class DocumentPageTransformationManager(models.Manager):
    def get_for_document_page(self, document_page):
        return self.model.objects.filter(document_page=document_page)

    def get_for_document_page_as_list(self, document_page):
        warnings = []
        transformations = []
        for transformation in self.get_for_document_page(document_page).values('transformation', 'arguments'):
            try:
                transformations.append(
                    {
                        'transformation': transformation['transformation'],
                        'arguments': literal_eval(transformation['arguments'].strip())
                    }
                )
            except (ValueError, SyntaxError), e:
                warnings.append(e)

        return transformations, warnings


class RecentDocumentManager(models.Manager):
    def add_document_for_user(self, user, document):
        from .settings import RECENT_COUNT

        if user.is_authenticated():
            new_recent, created = self.model.objects.get_or_create(user=user, document=document)
            if not created:
                # document already in the recent list, just update the accessed date and time
                new_recent.datetime_accessed = datetime.datetime.now()
                new_recent.save()
            for recent_to_delete in self.model.objects.filter(user=user)[RECENT_COUNT:]:
                recent_to_delete.delete()

    def get_for_user(self, user):
        #document_model = models.get_model('documents', 'Document')
        document_model = models.get_model('documents', 'document')
        if user.is_authenticated():
            return document_model.objects.filter(recentdocument__user=user).order_by('-recentdocument__datetime_accessed')
        else:
            return document_model.objects.none()


class DocumentTypeManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)
