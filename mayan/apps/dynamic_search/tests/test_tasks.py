from django.db import models

from mayan.apps.testing.tests.base import BaseTestCase

from ..classes import SearchBackend, SearchModel

from .mixins import SearchTaskTestMixin, SearchTestMixin


class SearchTaskTestCase(SearchTaskTestMixin, SearchTestMixin, BaseTestCase):
    auto_create_test_object_model = True
    auto_create_test_object_fields = {
        'test_field': models.CharField(max_length=8)
    }

    def _do_search(self, search_terms):
        return self.search_backend.search(
            search_model=self.test_model_search,
            query={
                'test_field': search_terms
            }, user=self._test_case_user
        )

    def _setup_test_model_search(self):
        self.test_model_search = SearchModel(
            app_label=self.TestModel._meta.app_label,
            model_name=self.TestModel._meta.model_name,
        )
        self.test_model_search.add_model_field(field='test_field')

    def setUp(self):
        super().setUp()
        self._create_test_object(instance_kwargs={'test_field': 'abc'})

        backend = SearchBackend.get_instance()
        backend.reset()

    def test_task_index_search_model(self):
        queryset = self._do_search(
            search_terms=self.test_objects[0].test_field
        )
        self.assertFalse(self.test_objects[0] in queryset)

        self._execute_task_index_search_model()

        queryset = self._do_search(
            search_terms=self.test_objects[0].test_field
        )
        self.assertTrue(self.test_objects[0] in queryset)

    def test_task_reindex_backend(self):
        queryset = self._do_search(
            search_terms=self.test_objects[0].test_field
        )
        self.assertFalse(self.test_objects[0] in queryset)

        self._execute_task_reindex_backend()

        queryset = self._do_search(
            search_terms=self.test_objects[0].test_field
        )
        self.assertTrue(self.test_objects[0] in queryset)
