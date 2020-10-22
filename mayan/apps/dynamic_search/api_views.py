from django.utils.encoding import force_text

from rest_framework.exceptions import ParseError

from mayan.apps.rest_api import generics

from .classes import SearchModel
from .mixins import SearchModelAPIMixin
from .serializers import SearchModelSerializer
from .runtime import search_backend


class APISearchView(SearchModelAPIMixin, generics.ListAPIView):
    """
    get: Perform a search operation
    """
    def get_queryset(self):
        search_model = self.get_search_model()

        # Override serializer class just before producing the queryset of
        # search results
        self.serializer_class = search_model.serializer

        if search_model.permission:
            self.mayan_object_permissions = {'GET': (search_model.permission,)}

        try:
            queryset = search_backend.search(
                search_model=search_model,
                query_string=self.request.GET, user=self.request.user
            )
        except Exception as exception:
            raise ParseError(force_text(s=exception))

        return queryset

    def get_serializer(self, *args, **kwargs):
        if self.get_search_model_name():
            return super(APISearchView, self).get_serializer(*args, **kwargs)
        else:
            return None


class APIAdvancedSearchView(SearchModelAPIMixin, generics.ListAPIView):
    """
    get: Perform an advanced search operation
    """
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
            queryset = search_backend.search(
                global_and_search=global_and_search,
                query_string=self.request.GET,
                search_model=self.search_model, user=self.request.user
            )
        except Exception as exception:
            raise ParseError(force_text(s=exception))

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
