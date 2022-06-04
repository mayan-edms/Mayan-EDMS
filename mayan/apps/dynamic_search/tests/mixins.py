from mayan.apps.documents.search import search_model_document

from ..classes import SearchBackend, SearchModel
from ..literals import QUERY_PARAMETER_ANY_FIELD, SEARCH_MODEL_NAME_KWARG
from ..tasks import task_reindex_backend, task_index_instances

from .backends import TestSearchBackend


class SearchTaskTestMixin:
    def _execute_task_reindex_backend(self):
        task_reindex_backend.apply_async().get()

    def _execute_task_index_instances(self):
        task_index_instances.apply_async(
            kwargs={
                'id_list': (self._test_object.pk,),
                'search_model_full_name': self._test_model_search.get_full_name()
            }
        ).get()


class SearchTestMixin:
    def _deindex_instance(self, instance):
        self.search_backend.deindex_instance(instance=instance)

    def _index_instance(self, instance):
        self.search_backend.index_instance(instance=instance)

    def _setup_test_model_search(self):
        """
        This method allows tests to add model search configurations and
        not have to import and initialize the SearchBackend.
        """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        TestSearchBackend._test_class = cls
        cls.search_backend = SearchBackend.get_instance()

    @classmethod
    def tearDownClass(cls):
        cls.search_backend.tear_down()
        cls.search_backend.close()
        super().tearDownClass()

    def setUp(self):
        self._existing_search_models = SearchModel._registry.copy()
        super().setUp()
        # Monkeypatch the search class so that the test behavior is only
        # enabled when called from a search test.
        self._setup_test_model_search()
        SearchBackend._enable()

    def tearDown(self):
        SearchBackend._disable()
        super().tearDown()
        SearchModel._registry = self._existing_search_models


class SearchAPIViewTestMixin(SearchTestMixin):
    def _request_search_view(self, search_model_name=None, search_term=None):
        query = {
            QUERY_PARAMETER_ANY_FIELD: search_term or self._test_document.label
        }
        search_model_name = search_model_name or search_model_document.get_full_name()

        return self.get(
            viewname='rest_api:search-view', kwargs={
                SEARCH_MODEL_NAME_KWARG: search_model_name
            }, query=query
        )

    def _request_advanced_search_view(
        self, search_model_name=None, search_term=None
    ):
        query = {
            'document_type__label': search_term or self._test_document.document_type.label
        }
        search_model_name = search_model_name or search_model_document.get_full_name()

        return self.get(
            viewname='rest_api:advanced-search-view', kwargs={
                SEARCH_MODEL_NAME_KWARG: search_model_name
            }, query=query
        )


class SearchToolsViewTestMixin(SearchTestMixin):
    def _request_search_backend_reindex_view(self):
        return self.post(viewname='search:search_backend_reindex')


class SearchViewTestMixin(SearchTestMixin):
    def _request_search_results_view(self, data, kwargs=None, query=None):
        return self.get(
            viewname='search:results', kwargs=kwargs, data=data, query=query
        )
