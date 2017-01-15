from __future__ import unicode_literals

from rest_framework import generics
from rest_framework.exceptions import ParseError

from rest_api.filters import MayanObjectPermissionsFilter

from .mixins import SearchModelMixin


class APISearchView(SearchModelMixin, generics.ListAPIView):
    """
    Perform a search operation
    ---
    GET:
        omit_serializer: true
        parameters:
            - name: search_model
              paramType: path
              type: string
              required: true
              description: Possible values are "documents.Document" or "document.DocumentPageResult"
            - name: q
              paramType: query
              type: string
              description: Term that will be used for the search.
    """

    filter_backends = (MayanObjectPermissionsFilter,)

    def get_queryset(self):
        search_model = self.get_search_model()

        # Override serializer class just before producing the queryset of
        # search results
        self.serializer_class = search_model.serializer

        if search_model.permission:
            self.mayan_object_permissions = {'GET': (search_model.permission,)}

        try:
            queryset, ids, timedelta = search_model.search(
                query_string=self.request.GET, user=self.request.user
            )
        except Exception as exception:
            raise ParseError(unicode(exception))

        return queryset


class APIAdvancedSearchView(SearchModelMixin, generics.ListAPIView):
    """
    Perform an advanced search operation
    ---
    GET:
        omit_serializer: true
        parameters:
            - name: search_model
              paramType: path
              type: string
              required: true
              description: Possible values are "documents.Document" or "document.DocumentPageResult"
            - name: _match_all
              paramType: query
              type: string
              description: When checked, only results that match all fields will be returned. When unchecked results that match at least one field will be returned. Possible values are "on" or "off"
    """

    filter_backends = (MayanObjectPermissionsFilter,)

    def get_queryset(self):
        self.search_model = self.get_search_model()

        # Override serializer class just before producing the queryset of
        # search results
        self.serializer_class = self.search_model.serializer

        if self.search_model.permission:
            self.mayan_object_permissions = {
                'GET': (self.search_model.permission,)
            }

        if self.request.GET.get('_match_all', 'off') == 'on':
            global_and_search = True
        else:
            global_and_search = False

        try:
            queryset, ids, timedelta = self.search_model.search(
                query_string=self.request.GET, user=self.request.user,
                global_and_search=global_and_search
            )
        except Exception as exception:
            raise ParseError(unicode(exception))

        return queryset
