from __future__ import unicode_literals

from rest_framework import generics
from rest_framework.exceptions import ParseError

from rest_api.filters import MayanObjectPermissionsFilter

from .classes import SearchModel
from .filters import RecentSearchUserFilter
from .models import RecentSearch
from .serializers import RecentSearchSerializer


class APIRecentSearchListView(generics.ListAPIView):
    """
    Returns a list of all the recent searches for the logged user.
    """

    filter_backends = (RecentSearchUserFilter,)
    queryset = RecentSearch.objects.all()
    serializer_class = RecentSearchSerializer


class APIRecentSearchView(generics.RetrieveAPIView):
    """
    Returns the selected recent search details.
    """

    filter_backends = (RecentSearchUserFilter,)
    queryset = RecentSearch.objects.all()
    serializer_class = RecentSearchSerializer


class APISearchView(generics.ListAPIView):
    """
    Perform a search operaton
    q -- Term that will be used for the search.
    """

    filter_backends = (MayanObjectPermissionsFilter,)

    def get_queryset(self):
        search_class = self.get_search_class()
        if search_class.permission:
            self.mayan_object_permissions = {'GET': (search_class.permission,)}

        try:
            queryset, ids, timedelta = search_class.search(
                query_string=self.request.GET, user=self.request.user
            )
        except Exception as exception:
            raise ParseError(unicode(exception))

        return queryset

    def get_search_class(self):
        return SearchModel.get('documents.Document')

    def get_serializer_class(self):
        return self.get_search_class().serializer
