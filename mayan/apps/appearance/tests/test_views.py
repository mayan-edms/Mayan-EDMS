from __future__ import absolute_import, unicode_literals

from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.firefox.webdriver import WebDriver

from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse

from mayan.apps.common.tests.base import GenericViewTestCase


class BasePlainViewTestCase(GenericViewTestCase, StaticLiveServerTestCase):
    auto_add_test_view = True
    test_view_url = r'^javascript:alert\("XSS"\)/$'
    test_view_is_public = True
    test_view_template = 'javascript_view'

    @classmethod
    def setUpClass(cls):
        super(BasePlainViewTestCase, cls).setUpClass()
        cls.selenium = WebDriver(log_path='/dev/null')

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(BasePlainViewTestCase, cls).tearDownClass()

    def test_login_view_url_fragment_xss(self):
        # Should redirect and not display an alert
        url = '{}{}{}'.format(
            self.live_server_url, reverse(viewname=settings.LOGIN_URL),
            '#javascript:alert("XSS")'
        )
        self.selenium.get(url=url)

        with self.assertRaises(NoAlertPresentException):
            self.selenium.switch_to_alert()

    def test_login_view_url_redirect(self):
        url = '{}{}{}'.format(
            self.live_server_url, reverse(viewname=settings.LOGIN_URL),
            '#javascript:alert("XSS")'
        )
        self.selenium.get(url=url)

        self.assertTrue(self.test_view_template in self.selenium.page_source)
