from django.apps import apps
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

from ..classes import ErrorLog

from .literals import TEST_ERROR_LOG_ENTRY_RESULT


class LoggingTextMixin:
    def _create_error_log_test_object(self):
        self._create_test_user()
        self.test_model = get_user_model()
        self.test_object = self.test_user

    def _create_error_log_entry(self):
        app_config = apps.get_app_config(app_label='logging')
        self.error_log = ErrorLog(app_config=app_config)
        self.error_log.register_model(
            model=self.test_model, register_permission=True
        )

        self.error_log_entry = self.test_object.error_log.create(
            text=TEST_ERROR_LOG_ENTRY_RESULT
        )


class LoggingViewTestMixin:
    def _request_object_error_log_list_view(self):
        content_type = ContentType.objects.get_for_model(
            model=self.test_object
        )

        return self.get(
            viewname='logging:object_error_list', kwargs={
                'app_label': content_type.app_label,
                'model_name': content_type.model,
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
                'model_name': content_type.model,
                'object_id': self.test_object.pk
            }
        )
