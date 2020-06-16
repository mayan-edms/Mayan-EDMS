from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

from mayan.apps.acls.classes import ModelPermission
from mayan.apps.tests.tests.base import GenericViewTestCase

from ..models import ErrorLogEntry
from ..permissions_runtime import permission_error_log_view

from .literals import TEST_ERROR_LOG_ENTRY_RESULT


class CommonViewTestMixin:
    def _request_about_view(self):
        return self.get(viewname='common:about_view')

    def _request_object_error_log_list(self):
        content_type = ContentType.objects.get_for_model(model=self.test_user)

        return self.get(
            viewname='common:object_error_list', kwargs={
                'app_label': content_type.app_label,
                'model_name': content_type.model,
                'object_id': self.test_user.pk
            }
        )


class CommonViewTestCase(CommonViewTestMixin, GenericViewTestCase):
    def test_about_view(self):
        response = self._request_about_view()
        self.assertContains(response=response, text='About', status_code=200)
