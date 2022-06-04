from django.utils.encoding import force_text

from rest_framework.exceptions import ParseError

from mayan.apps.rest_api import generics

from .api_view_mixins import SearchModelAPIViewMixin
from .classes import SearchBackend, SearchModel
from .serializers import SearchModelSerializer
from .utils import get_match_all_value


class APISearchView(SearchModelAPIViewMixin, generics.ListAPIView):
    """
    get: Perform a search operation
    """
    def get_queryset(self):
        search_model = self.get_search_model()

        # Override serializer class just before producing the queryset of
        # search results.
        self.serializer_class = search_model.serializer

        if search_model.permission:
            self.mayan_object_permissions = {
                'GET': (search_model.permission,)
            }

        query_dict = self.request.GET.dict().copy()
        query_dict.update(self.request.POST.dict())

        try:
            queryset = SearchBackend.get_instance().search(
                search_model=search_model, query=query_dict,
                user=self.request.user
            )
        except Exception as exception:
            raise ParseError(force_text(s=exception))

        return queryset

    def get_serializer(self, *args, **kwargs):
        if self.get_search_model_name():
            return super().get_serializer(*args, **kwargs)
        else:
            return None


class APIAdvancedSearchView(SearchModelAPIViewMixin, generics.ListAPIView):
    """
    get: Perform an advanced search operation
    """
    def get_queryset(self):
        self.search_model = self.get_search_model()

        # Override serializer class just before producing the queryset of
        # search results.
        self.serializer_class = self.search_model.serializer

        if self.search_model.permission:
            self.mayan_object_permissions = {
                'GET': (self.search_model.permission,)
            }

        query_dict = self.request.GET.dict().copy()
        query_dict.update(self.request.POST.dict())

        global_and_search = get_match_all_value(
            value=query_dict.get('_match_all')
        )

        try:
            queryset = SearchBackend.get_instance().search(
                global_and_search=global_and_search, query=query_dict,
                search_model=self.search_model, user=self.request.user
            )
        except Exception as exception:
            raise ParseError(force_text(s=exception))

        return queryset

    def get_serializer(self, *args, **kwargs):
        if self.get_search_model_name():
            return super().get_serializer(*args, **kwargs)
        else:
            return None


class APISearchModelList(generics.ListAPIView):
    """
    get: Returns a list of all the available search models.
    """
    serializer_class = SearchModelSerializer

    def get_queryset(self):
        # This changes after the initial startup as search models are
        # automatically loaded.
        return SearchModel.all()
