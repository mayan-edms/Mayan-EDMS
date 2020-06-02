from rest_framework.test import APITestCase

from mayan.apps.tests.tests.base import GenericViewTestCase
from mayan.apps.permissions.classes import Permission
from mayan.apps.smart_settings.classes import SettingNamespace


class BaseAPITestCase(APITestCase, GenericViewTestCase):
    """
    API test case class that invalidates permissions and smart settings
    """
    expected_content_types = None

    def setUp(self):
        super(BaseAPITestCase, self).setUp()
        SettingNamespace.invalidate_cache_all()
        Permission.invalidate_cache()
