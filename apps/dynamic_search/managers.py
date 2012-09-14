from __future__ import absolute_import

from urlparse import urlparse, parse_qs
from urllib import unquote_plus

from django.utils.simplejson import dumps
from django.db.models import Manager
from django.contrib.auth.models import AnonymousUser
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import smart_str


class RecentSearchManager(Manager):
    def add_query_for_user(self, search_view):
        from .settings import RECENT_COUNT

        query_dict = parse_qs(unquote_plus(smart_str(urlparse(search_view.request.get_full_path()).query)))

        if query_dict and not isinstance(search_view.request.user, AnonymousUser):
            # If the URL query has at least one variable with a value
            new_recent, created = self.model.objects.get_or_create(user=search_view.request.user, query=dumps(query_dict), defaults={'hits': 0})
            new_recent.hits = search_view.results.count()
            new_recent.save()
            to_delete = self.model.objects.filter(user=search_view.request.user)[RECENT_COUNT:]
            for recent_to_delete in to_delete:
                recent_to_delete.delete()

    def get_for_user(self, user):
        return [entry for entry in self.model.objects.filter(user=user) if entry.get_query()]


class IndexableObjectManager(Manager):
    def get_indexables(self, datetime=None):
        if datetime:
            return self.model.objects.filter(datetime__gte=datetime)
        else:
            return self.model.objects.all()

    def get_indexables_pk_list(self, datetime=None):
        return self.get_indexables(datetime).values_list('object_id', flat=True)

    def mark_indexable(self, obj):
        content_type = ContentType.objects.get_for_model(obj)
        self.model.objects.get_or_create(content_type=content_type, object_id=obj.pk)

    def clear_all(self):
        self.model.objects.all().delete()
