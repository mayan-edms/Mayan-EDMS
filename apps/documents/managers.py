from __future__ import absolute_import

from ast import literal_eval
from datetime import datetime

from django.db import models
from django.contrib.auth.models import AnonymousUser

from .conf.settings import RECENT_COUNT


class RecentDocumentManager(models.Manager):
    def add_document_for_user(self, user, document):
        self.model.objects.filter(user=user, document=document).delete()
        new_recent = self.model(user=user, document=document, datetime_accessed=datetime.now())
        new_recent.save()
        to_delete = self.model.objects.filter(user=user)[RECENT_COUNT:]
        for recent_to_delete in to_delete:
            recent_to_delete.delete()
            
    def get_for_user(self, user):
        if not user.is_anonymous():
            return [recent_document.document for recent_document in self.model.objects.filter(user=user)]
        else:
            return []


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
