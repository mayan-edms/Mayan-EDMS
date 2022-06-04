import json

from mayan.apps.documents.tests.literals import TEST_FILE_SMALL_PATH

from ...source_backends.literals import SOURCE_UNCOMPRESS_CHOICE_NEVER
from ...source_backends.web_form_backends import SourceBackendWebForm

from .base_mixins import SourceTestMixin


class WebFormSourceBackendAPITestMixin:
    def _request_test_web_form_file_upload_action_api_view(self, test_file_path=TEST_FILE_SMALL_PATH):
        with open(file=test_file_path, mode='rb') as file_object:
            return self.post(
                viewname='rest_api:source-action', kwargs={
                    'action_name': 'upload', 'source_id': self._test_source.pk
                }, data={
                    'arguments': json.dumps(
                        obj={
                            'document_type_id': self._test_document_type.pk,
                            'expand': True
                        }
                    ), 'file': file_object
                }
            )


class WebFormSourceBackendTestMixin(SourceTestMixin):
    _create_source_method = '_create_test_web_form_source'

    def _create_test_web_form_source(self, extra_data=None):
        backend_data = {'uncompress': SOURCE_UNCOMPRESS_CHOICE_NEVER}

        if extra_data:
            backend_data.update(extra_data)

        self._create_test_source(
            backend_path=SourceBackendWebForm.get_class_path(),
            backend_data=backend_data
        )
