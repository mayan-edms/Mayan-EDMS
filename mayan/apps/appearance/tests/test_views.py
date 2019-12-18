from __future__ import absolute_import, unicode_literals

from selenium.webdriver.firefox.webdriver import WebDriver

from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse


class BasePlainViewTestCase(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super(BasePlainViewTestCase, cls).setUpClass()
        cls.selenium = WebDriver()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(BasePlainViewTestCase, cls).tearDownClass()

    def test_login_view_url_fragment_xss(self):
        url = '{}{}{}'.format(
            self.live_server_url, reverse(viewname=settings.LOGIN_URL),
            '#javascript:alert("XSS")'
        )
        self.selenium.get(url=url)
        self.selenium.find_element_by_xpath(xpath='//button[@name="submit"]')
