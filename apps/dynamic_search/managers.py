import urlparse
from datetime import datetime

from django.db import models
from django.utils.http import urlencode

from dynamic_search.conf.settings import RECENT_COUNT


class RecentSearchManager(models.Manager):
    def add_query_for_user(self, user, query, hits):
        parsed_query = urlparse.parse_qs(query)
        if ('q=' in query) and not parsed_query.get('q'):
            # Don't store empty simple searches
            return
        else:
            parsed_query = {'q': u' '.join(parsed_query['q'])}
        if parsed_query:
            # If the URL query has at least one variable with a value
            new_recent, created = self.model.objects.get_or_create(user=user, query=urlencode(parsed_query), defaults={'hits': hits})
            new_recent.hits = hits
            new_recent.save()
            to_delete = self.model.objects.filter(user=user)[RECENT_COUNT:]
            for recent_to_delete in to_delete:
                recent_to_delete.delete()
