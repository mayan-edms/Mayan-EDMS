from django.apps import apps
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

from mayan.apps.tests.tests.base import GenericViewTestCase

from ..classes import ErrorLog
from ..permissions import permission_error_log_view


class LoggingViewTestMixin:
    def _request_object_error_log_list_view(self):
        content_type = ContentType.objects.get_for_model(
            model=self.test_object
        )

        return self.get(
            viewname='logging:object_error_list', kwargs={
                'app_label': content_type.app_label,
                'model': content_type.model,
                'object_id': self.test_object.pk
            }
        )

    def _request_object_error_log_list_clear_view(self):
        content_type = ContentType.objects.get_for_model(
            model=self.test_object
        )

        return self.post(
            viewname='logging:object_error_list_clear', kwargs={
                'app_label': content_type.app_label,
                'model': content_type.model,
                'object_id': self.test_object.pk
            }
        )
