from mayan.apps.document_states import storages
from mayan.apps.smart_settings.tests.mixins import SmartSettingTestMixin
from mayan.apps.storage.tests.mixins import StorageSettingTestMixin
from mayan.apps.testing.tests.base import BaseTestCase

from ..literals import STORAGE_NAME_WORKFLOW_CACHE
from ..settings import setting_workflow_image_cache_storage_backend_arguments


class WorkflowStorageSettingsTestCase(
    SmartSettingTestMixin, StorageSettingTestMixin, BaseTestCase
):
    def test_setting_workflow_image_cache_storage_backend_arguments_invalid_value(self):
        assertion = self._test_storage_setting_with_invalid_value(
            setting=setting_workflow_image_cache_storage_backend_arguments,
            storage_module=storages,
            storage_name=STORAGE_NAME_WORKFLOW_CACHE
        )

        self.assertTrue('Unable to initialize' in str(assertion.exception))
        self.assertTrue('workflow preview' in str(assertion.exception))
