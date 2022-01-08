from io import StringIO
from unittest import skip

from django.core import management
from django.db import models

from mayan.apps.testing.tests.base import BaseTestCase
from mayan.apps.testing.tests.utils import mute_stdout

from ..classes import SearchBackend, SearchModel

from .mixins import SearchTestMixin


class SearchIndexObjectManagementCommandTestCaseMixin(SearchTestMixin):
    auto_create_test_object_model = True
    auto_create_test_object_fields = {
        'test_field': models.CharField(max_length=8)
    }

    def _call_command(self, id_range_string):
        with mute_stdout():
            management.call_command(
                'search_index_objects',
                self._test_model_search.get_full_name(), id_range_string
            )

    def _do_search(self, search_terms):
        return self.search_backend.search(
            search_model=self._test_model_search,
            query={
                'test_field': search_terms
            }, user=self._test_case_user
        )

    def _setup_test_model_search(self):
        self._test_model_search = SearchModel(
            app_label=self.TestModel._meta.app_label,
            model_name=self.TestModel._meta.model_name,
        )
        self._test_model_search.add_model_field(field='test_field')

    def test_command_calling(self):
        self._create_test_object(instance_kwargs={'test_field': 'abc'})

        backend = SearchBackend.get_instance()
        backend.reset()

        self._call_command(id_range_string=self.test_objects[0].pk)

    def test_command_artifacts(self):
        self._create_test_object(instance_kwargs={'test_field': 'abc'})
        self._create_test_object(instance_kwargs={'test_field': 'xyz'})

        queryset = self._do_search(
            search_terms=self.test_objects[0].test_field
        )
        self.assertTrue(self.test_objects[0] in queryset)

        queryset = self._do_search(
            search_terms=self.test_objects[1].test_field
        )
        self.assertTrue(self.test_objects[1] in queryset)

        backend = SearchBackend.get_instance()
        backend.reset()

        queryset = self._do_search(
            search_terms=self.test_objects[0].test_field
        )
        self.assertTrue(self.test_objects[0] not in queryset)

        queryset = self._do_search(
            search_terms=self.test_objects[1].test_field
        )
        self.assertTrue(self.test_objects[1] not in queryset)

        self._call_command(id_range_string=self.test_objects[0].pk)

        queryset = self._do_search(
            search_terms=self.test_objects[0].test_field
        )
        self.assertTrue(self.test_objects[0] in queryset)

        queryset = self._do_search(
            search_terms=self.test_objects[1].test_field
        )
        self.assertTrue(self.test_objects[1] not in queryset)

        self._call_command(id_range_string=self.test_objects[1].pk)

        queryset = self._do_search(
            search_terms=self.test_objects[0].test_field
        )
        self.assertTrue(self.test_objects[0] in queryset)

        queryset = self._do_search(
            search_terms=self.test_objects[1].test_field
        )
        self.assertTrue(self.test_objects[1] in queryset)


class DjangoSearchIndexObjectManagementCommandTestCase(
    SearchIndexObjectManagementCommandTestCaseMixin, BaseTestCase
):
    _test_search_backend_path = 'mayan.apps.dynamic_search.backends.django.DjangoSearchBackend'
    """Test against Django backend."""

    @skip('Backend does not support indexing.')
    def test_command_artifacts(self):
        """Backend does not support indexing."""


@skip('Skip until a Mock ElasticSearch server class is added.')
class ElasticSearchIndexObjectManagementCommandTestCase(
    SearchIndexObjectManagementCommandTestCaseMixin, BaseTestCase
):
    _test_search_backend_path = 'mayan.apps.dynamic_search.backends.elasticsearch.ElasticSearchBackend'
    """Test against ElasticSearch backend."""


class WhooshSearchIndexObjectManagementCommandTestCase(
    SearchIndexObjectManagementCommandTestCaseMixin, BaseTestCase
):
    _test_search_backend_path = 'mayan.apps.dynamic_search.backends.whoosh.WhooshSearchBackend'
    """Test against Whoosh backend."""


class SearchStatusManagementCommandTestCaseMixin(SearchTestMixin):
    _ignore_result = False
    auto_create_test_object_model = True
    auto_create_test_object_fields = {
        'test_field': models.CharField(max_length=8)
    }

    def _do_search(self, search_terms):
        return self.search_backend.search(
            search_model=self._test_model_search,
            query={
                'test_field': search_terms
            }, user=self._test_case_user
        )

    def _setup_test_model_search(self):
        self._test_model_search = SearchModel(
            app_label=self.TestModel._meta.app_label,
            model_name=self.TestModel._meta.model_name,
        )
        self._test_model_search.add_model_field(field='test_field')

    def test_command(self):
        backend = SearchBackend.get_instance()
        backend.reset()

        self._create_test_object(instance_kwargs={'test_field': 'abc'})
        self._create_test_object(instance_kwargs={'test_field': 'xyz'})

        queryset = self._do_search(
            search_terms=self.test_objects[0].test_field
        )
        self.assertTrue(self.test_objects[0] in queryset)

        output = StringIO()
        options = {
            'stdout': output
        }

        management.call_command(command_name='search_status', **options)
        output.seek(0)

        count = 0

        lines = output.readlines()

        for line in lines:
            if self._test_model_search.model_name in line.lower():
                model_name, count = line.split(':')
                count = int(count)

        self.assertEqual(count, len(self.test_objects))


class DjangoSearchStatusManagementCommandTestCase(
    SearchStatusManagementCommandTestCaseMixin, BaseTestCase
):
    _test_search_backend_path = 'mayan.apps.dynamic_search.backends.django.DjangoSearchBackend'
    """Test against DjangoSearch backend."""


@skip('Skip until a Mock ElasticSearch server class is added.')
class ElasticSearchStatusManagementCommandTestCase(
    SearchStatusManagementCommandTestCaseMixin, BaseTestCase
):
    _test_search_backend_path = 'mayan.apps.dynamic_search.backends.elasticsearch.ElasticSearchBackend'
    """Test against ElasticSearch backend."""


class WhooshSearchStatusManagementCommandTestCase(
    SearchStatusManagementCommandTestCaseMixin, BaseTestCase
):
    _test_search_backend_path = 'mayan.apps.dynamic_search.backends.whoosh.WhooshSearchBackend'
    """Test against WhooshSearch backend."""
