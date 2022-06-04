from mayan.apps.dynamic_search.tests.mixins import SearchTestMixin
from mayan.apps.testing.tests.base import BaseTestCase

from ..permissions import permission_message_view
from ..search import search_model_message

from .mixins import MessageTestMixin


class MessageSearchTestCase(
    MessageTestMixin, SearchTestMixin, BaseTestCase
):
    def setUp(self):
        super().setUp()
        self._create_test_message()

    def _do_test_search(self, query):
        return self.search_backend.search(
            search_model=search_model_message, query=query,
            user=self._test_case_user
        )

    def test_search_model_message_body_no_permission(self):
        self._clear_events()

        queryset = self._do_test_search(
            query={'body': self._test_message.body}
        )
        self.assertTrue(self._test_message not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_search_model_message_body_with_access(self):
        self.grant_access(
            obj=self._test_message, permission=permission_message_view
        )

        self._clear_events()

        queryset = self._do_test_search(
            query={'body': self._test_message.body}
        )
        self.assertTrue(self._test_message in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_search_model_message_date_year_no_permission(self):
        self._clear_events()

        queryset = self._do_test_search(
            query={'date_time': self._test_message.date_time.year}
        )
        self.assertTrue(self._test_message not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_search_model_message_date_year_with_access(self):
        self.grant_access(
            obj=self._test_message, permission=permission_message_view
        )

        self._clear_events()

        queryset = self._do_test_search(
            query={'date_time': self._test_message.date_time.year}
        )
        self.assertTrue(self._test_message in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_search_model_message_subject_no_permission(self):
        self._clear_events()

        queryset = self._do_test_search(
            query={'subject': self._test_message.subject}
        )
        self.assertTrue(self._test_message not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_search_model_message_subject_with_access(self):
        self.grant_access(
            obj=self._test_message, permission=permission_message_view
        )

        self._clear_events()

        queryset = self._do_test_search(
            query={'subject': self._test_message.subject}
        )
        self.assertTrue(self._test_message in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
