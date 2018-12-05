from __future__ import absolute_import, unicode_literals

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

from mayan.apps.acls import ModelPermission

from ..models import ErrorLogEntry
from ..permissions_runtime import permission_error_log_view

from .base import GenericViewTestCase
from .literals import TEST_ERROR_LOG_ENTRY_RESULT


class CommonViewTestCase(GenericViewTestCase):
    def test_about_view(self):
        self.login_user()

        response = self.get('common:about_view')
        self.assertContains(response, text='About', status_code=200)

    def _create_error_log_entry(self):
        ModelPermission.register(
            model=get_user_model(), permissions=(permission_error_log_view,)
        )
        ErrorLogEntry.objects.register(model=get_user_model())

        self.error_log_entry = self.user.error_logs.create(
            result=TEST_ERROR_LOG_ENTRY_RESULT
        )

    def _request_object_error_log_list(self):
        content_type = ContentType.objects.get_for_model(model=self.user)

        return self.get(
            'common:object_error_list', kwargs={
                'app_label': content_type.app_label,
                'model': content_type.model,
                'object_id': self.user.pk
            }, follow=True
        )

    def test_object_error_list_view_with_permissions(self):
            self._create_error_log_entry()

            self.login_user()
            self.grant_access(
                obj=self.user, permission=permission_error_log_view
            )

            response = self._request_object_error_log_list()

            self.assertContains(
                response=response, text=TEST_ERROR_LOG_ENTRY_RESULT,
                status_code=200
            )

    def test_object_error_list_view_no_permissions(self):
            self._create_error_log_entry()

            self.login_user()

            response = self._request_object_error_log_list()

            self.assertNotContains(
                response=response, text=TEST_ERROR_LOG_ENTRY_RESULT,
                status_code=403
            )
