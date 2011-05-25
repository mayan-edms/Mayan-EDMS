from datetime import datetime

from django.db import models

from documents.conf.settings import RECENT_COUNT


class RecentDocumentManager(models.Manager):
    def add_document_for_user(self, user, document):
        self.model.objects.filter(user=user, document=document).delete()
        new_recent = self.model(user=user, document=document, datetime_accessed=datetime.now())
        new_recent.save()
        to_delete = self.model.objects.filter(user=user)[RECENT_COUNT:]
        for recent_to_delete in to_delete:
            recent_to_delete.delete()
