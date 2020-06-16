from django.apps import apps
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

from mayan.apps.tests.tests.base import GenericViewTestCase

from ..classes import ErrorLog
from ..permissions import permission_error_log_view

from .literals import TEST_ERROR_LOG_ENTRY_RESULT
from .mixins import LoggingViewTestMixin


class LogingViewTestCase(LoggingViewTestMixin, GenericViewTestCase):
    def setUp(self):
        super().setUp()
        self._create_test_user()
        self.test_model = get_user_model()
        self.test_object = self.test_user
        self._create_error_log_entry()

    def _create_error_log_entry(self):
        app_config = apps.get_app_config(app_label='logging')
        error_log = ErrorLog(app_config=app_config)
        error_log.register_model(
            model=self.test_model, register_permission=True
        )

        self.error_log_entry = self.test_object.error_log.create(
            text=TEST_ERROR_LOG_ENTRY_RESULT
        )

    def test_object_error_list_view_no_permissions(self):
        response = self._request_object_error_log_list_view()
        self.assertNotContains(
            response=response, text=TEST_ERROR_LOG_ENTRY_RESULT,
            status_code=404
        )

    def test_object_error_list_view_with_access(self):
        self.grant_access(
            obj=self.test_object, permission=permission_error_log_view
        )

        response = self._request_object_error_log_list_view()
        self.assertContains(
            response=response, text=TEST_ERROR_LOG_ENTRY_RESULT,
            status_code=200
        )

    def test_object_error_list_clear_view_no_permission(self):
        response = self._request_object_error_log_list_clear_view()
        self.assertEqual(response.status_code, 404)

        self.assertNotEqual(self.test_object.error_log.count(), 0)

    def test_object_error_list_clear_view_with_access(self):
        self.grant_access(
            obj=self.test_object, permission=permission_error_log_view
        )

        response = self._request_object_error_log_list_clear_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(self.test_object.error_log.count(), 0)
