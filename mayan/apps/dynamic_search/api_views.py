from __future__ import absolute_import

from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from rest_framework import generics, status
from rest_framework.response import Response

from acls.models import AccessEntry
from permissions.models import Permission
from rest_api.filters import MayanObjectPermissionsFilter
from rest_api.permissions import MayanPermission

from .classes import SearchModel
from .models import RecentSearch
from .serializers import RecentSearchSerializer


class APIRecentSearchListView(generics.ListAPIView):
    """
    Returns a list of all the recent searches.
    """

    serializer_class = RecentSearchSerializer
    queryset = RecentSearch.objects.all()

    # TODO: Add filter_backend so that users can only see their own entries


class APIRecentSearchView(generics.RetrieveDestroyAPIView):
    """
    Returns the selected recent search details.
    """

    serializer_class = RecentSearchSerializer
    queryset = RecentSearch.objects.all()

    # TODO: Add filter_backend so that users can only see their own entries


class APISearchView(generics.ListAPIView):
    """
    Perform a search operaton
    q -- Term that will be used for the search.
    """

    def get_queryset(self):
        document_search = SearchModel.get('documents.Document')
        self.serializer_class = document_search.serializer

        if 'q' in self.request.GET:
            # Simple query
            query_string = self.request.GET.get('q', u'').strip()
            queryset, ids, timedelta = document_search.simple_search(query_string)
        else:
            # Advanced search
            queryset, ids, timedelta = document_search.advanced_search(self.request.GET)

        RecentSearch.objects.add_query_for_user(self.request.user, self.request.GET, len(ids))

        return queryset
