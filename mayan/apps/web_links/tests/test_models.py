from mayan.apps.tests.tests.base import BaseTestCase

from .mixins import WebLinkTestMixin


class WebLinkViewTestCase(WebLinkTestMixin, BaseTestCase):
    def test_method_get_absolute_url(self):
        self._create_test_web_link()

        self.assertTrue(self.test_web_link.get_absolute_url())
