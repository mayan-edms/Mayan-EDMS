from mayan.apps.common.settings import setting_home_view
from mayan.apps.common.tests.base import GenericViewTestCase
from mayan.apps.common.tests.utils import mute_stdout

from ..models import AutoAdminSingleton

from .literals import TEST_FIRST_TIME_LOGIN_TEXT, TEST_MOCK_VIEW_TEXT


class AutoAdminViewMixing(object):
    def _request_home_view(self):
        return self.get(viewname=setting_home_view.value, follow=True)


class AutoAdminViewCase(AutoAdminViewMixing, GenericViewTestCase):
    auto_create_group = False
    auto_create_users = False
    auto_login_user = False

    def setUp(self):
        super(AutoAdminViewCase, self).setUp()
        with mute_stdout():
            AutoAdminSingleton.objects.create_autoadmin()

    def test_login_302_view(self):
        response = self._request_home_view()

        self.assertContains(
            response=response, text=TEST_FIRST_TIME_LOGIN_TEXT,
            status_code=200
        )

    def test_login_ok_view(self):
        autoadmin = AutoAdminSingleton.objects.get()
        logged_in = self.login(
            username=autoadmin.account,
            password=autoadmin.password
        )
        self.assertTrue(logged_in)

        response = self._request_home_view()

        self.assertNotContains(
            response=response, text=TEST_MOCK_VIEW_TEXT,
            status_code=200
        )
