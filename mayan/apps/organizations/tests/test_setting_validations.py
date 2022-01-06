from django.core.exceptions import ValidationError

from mayan.apps.testing.tests.base import BaseTestCase

from ..settings import setting_organization_url_base_path

from .literals import (
    TEST_PATH_GOOD, TEST_PATH_WITH_ENDING_SLASH,
    TEST_PATH_WITH_INITIAL_SLASH
)


class OrganizationSettingValidationTestCase(BaseTestCase):
    def test_url_base_path_initial_slash_validation(self):
        with self.assertRaises(expected_exception=ValidationError):
            setting_organization_url_base_path.validate(
                raw_value=TEST_PATH_WITH_INITIAL_SLASH
            )

    def test_url_base_path_initial_ending_validation(self):
        with self.assertRaises(expected_exception=ValidationError):
            setting_organization_url_base_path.validate(
                raw_value=TEST_PATH_WITH_ENDING_SLASH
            )

    def test_url_base_path_good_value_validation(self):
        setting_organization_url_base_path.validate(
            raw_value=TEST_PATH_GOOD
        )

    def test_url_base_path_none_value_validation(self):
        setting_organization_url_base_path.validate(
            raw_value=None
        )
