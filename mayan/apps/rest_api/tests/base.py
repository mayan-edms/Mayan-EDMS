from rest_framework.test import APITestCase, APITransactionTestCase

from mayan.apps.permissions.classes import Permission
from mayan.apps.smart_settings.classes import SettingNamespace
from mayan.apps.testing.tests.base import (
    GenericViewTestCase, GenericTransactionViewTestCase
)


class BaseAPITestCase(APITestCase, GenericViewTestCase):
    """
    API test case class that invalidates permissions and smart settings.
    """
    expected_content_types = None

    def setUp(self):
        super().setUp()
        SettingNamespace.invalidate_cache_all()
        Permission.invalidate_cache()


class BaseAPITransactionTestCase(
    APITransactionTestCase, GenericTransactionViewTestCase
):
    """
    API transaction test case class that invalidates permissions and smart
    settings.
    """
    expected_content_types = None

    def setUp(self):
        super().setUp()
        SettingNamespace.invalidate_cache_all()
        Permission.invalidate_cache()
