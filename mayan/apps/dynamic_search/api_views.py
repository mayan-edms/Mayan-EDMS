from __future__ import unicode_literals

from django.utils.encoding import force_text

from rest_framework import generics
from rest_framework.exceptions import ParseError

from rest_api.filters import MayanObjectPermissionsFilter

from .classes import SearchModel
from .mixins import SearchModelMixin
from .serializers import SearchModelSerializer


class APISearchView(SearchModelMixin, generics.ListAPIView):
    """
    get: Perform a search operation
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
            queryset, timedelta = search_model.search(
                query_string=self.request.GET, user=self.request.user
            )
        except Exception as exception:
            raise ParseError(force_text(exception))

        return queryset

    def get_serializer(self, *args, **kwargs):
        if self.get_search_model_name():
            return super(APISearchView, self).get_serializer(*args, **kwargs)
        else:
            return None


class APIAdvancedSearchView(SearchModelMixin, generics.ListAPIView):
    """
    get: Perform an advanced search operation
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
            queryset, timedelta = self.search_model.search(
                query_string=self.request.GET, user=self.request.user,
                global_and_search=global_and_search
            )
        except Exception as exception:
            raise ParseError(force_text(exception))

        return queryset

    def get_serializer(self, *args, **kwargs):
        if self.get_search_model_name():
            return super(APIAdvancedSearchView, self).get_serializer(*args, **kwargs)
        else:
            return None


class APISearchModelList(generics.ListAPIView):
    """
    get: Returns a list of all the available search models.
    """
    serializer_class = SearchModelSerializer
    queryset = SearchModel.all()
