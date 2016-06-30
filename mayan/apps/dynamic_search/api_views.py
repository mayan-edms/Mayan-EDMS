from __future__ import unicode_literals

from rest_framework import generics
from rest_framework.exceptions import ParseError

from rest_api.filters import MayanObjectPermissionsFilter

from .classes import SearchModel


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
