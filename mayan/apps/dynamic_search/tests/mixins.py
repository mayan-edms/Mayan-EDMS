from mayan.apps.documents.search import document_search
from mayan.apps.storage.utils import fs_cleanup, mkdtemp

from ..classes import SearchBackend
from ..settings import setting_backend_arguments


class SearchAPIViewTestMixin:
    def _request_search_view(self):
        query = {'q': self.test_document.label}
        return self.get(
            viewname='rest_api:search-view', kwargs={
                'search_model_name': document_search.get_full_name()
            }, query=query
        )

    def _request_advanced_search_view(self):
        query = {'document_type__label': self.test_document.document_type.label}

        return self.get(
            viewname='rest_api:advanced-search-view', kwargs={
                'search_model_name': document_search.get_full_name()
            }, query=query
        )


class SearchTestMixin:
    def setUp(self):
        self.old_value = setting_backend_arguments.value
        super().setUp()
        setting_backend_arguments.set(
            value={'index_path': mkdtemp()}
        )
        self.search_backend = SearchBackend.get_instance()

    def tearDown(self):
        fs_cleanup(
            filename=setting_backend_arguments.value['index_path']
        )
        setting_backend_arguments.set(value=self.old_value)
        super().tearDown()


class SearchToolsViewTestMixin:
    def _request_search_backend_reindex_view(self):
        return self.post(viewname='search:search_backend_reindex')


class SearchViewTestMixin:
    def _request_search_results_view(self, data, kwargs=None, query=None):
        return self.get(
            viewname='search:results', kwargs=kwargs, data=data, query=query
        )
