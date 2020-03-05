from __future__ import absolute_import, unicode_literals

from unittest import skip

from selenium.common.exceptions import NoAlertPresentException

from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from mayan.apps.common.tests.base import GenericViewTestCase
from mayan.apps.common.tests.mixins import SeleniumTestMixin


@skip('Skip until a synchronous live server class is added.')
class BasePlainViewTestCase(
    SeleniumTestMixin, StaticLiveServerTestCase, GenericViewTestCase
):
    auto_add_test_view = True
    test_view_url = r'^javascript:alert\("XSS"\)/$'
    test_view_is_public = True
    test_view_template = 'javascript_view'

    def test_login_view_url_fragment_xss(self):
        # Should redirect and not display an alert
        self._open_url(
            fragment='#javascript:alert("XSS")', viewname=settings.LOGIN_URL
        )

        with self.assertRaises(NoAlertPresentException):
            self.webdriver.switch_to_alert()

    def test_login_view_url_redirect(self):
        self._open_url(
            fragment='#javascript:alert("XSS")', viewname=settings.LOGIN_URL
        )

        self.assertTrue(self.test_view_template in self.webdriver.page_source)
