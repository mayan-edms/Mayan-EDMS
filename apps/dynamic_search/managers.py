from datetime import datetime

from django.db import models

from dynamic_search.conf.settings import RECENT_COUNT


class RecentSearchManager(models.Manager):
    def add_query_for_user(self, user, query, hits):
        new_recent, created = self.model.objects.get_or_create(user=user, query=query)
        new_recent.hits = hits
        new_recent.save()
        to_delete = self.model.objects.filter(user=user)[RECENT_COUNT:]
        for recent_to_delete in to_delete:
            recent_to_delete.delete()
