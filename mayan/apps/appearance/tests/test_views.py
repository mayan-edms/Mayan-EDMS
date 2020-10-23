from unittest import skip

from selenium.common.exceptions import NoAlertPresentException

from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from mayan.apps.events.tests.mixins import EventTestCaseMixin
from mayan.apps.testing.tests.base import GenericViewTestCase
from mayan.apps.testing.tests.mixins import SeleniumTestMixin

from ..events import event_theme_created, event_theme_edited
from ..models import Theme
from ..permissions import (
    permission_theme_create, permission_theme_delete, permission_theme_edit,
    permission_theme_view
)

from .mixins import ThemeTestMixin, ThemeViewTestMixin


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

        with self.assertRaises(expected_exception=NoAlertPresentException):
            self.webdriver.switch_to_alert()

    def test_login_view_url_redirect(self):
        self._open_url(
            fragment='#javascript:alert("XSS")', viewname=settings.LOGIN_URL
        )

        self.assertTrue(self.test_view_template in self.webdriver.page_source)


class ThemeViewTestCase(
    EventTestCaseMixin, ThemeTestMixin, ThemeViewTestMixin, GenericViewTestCase
):
    _test_event_object_name = 'test_theme'

    def test_theme_create_view_no_permission(self):
        theme_count = Theme.objects.count()

        response = self._request_test_theme_create_view()
        self.assertEqual(response.status_code, 403)

        self.assertEqual(Theme.objects.count(), theme_count)

        event = self._get_test_object_event()
        self.assertEqual(event, None)

    def test_theme_create_view_with_permissions(self):
        self.grant_permission(permission=permission_theme_create)

        theme_count = Theme.objects.count()

        response = self._request_test_theme_create_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Theme.objects.count(), theme_count + 1)

        event = self._get_test_object_event()
        self.assertEqual(event.verb, event_theme_created.id)

    def test_theme_delete_view_no_permission(self):
        self._create_test_theme()

        theme_count = Theme.objects.count()

        response = self._request_test_theme_delete_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(Theme.objects.count(), theme_count)

        event = self._get_test_object_event()
        self.assertEqual(event.verb, event_theme_created.id)

    def test_theme_delete_view_with_access(self):
        self._create_test_theme()

        self.grant_access(
            obj=self.test_theme, permission=permission_theme_delete
        )

        theme_count = Theme.objects.count()

        response = self._request_test_theme_delete_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Theme.objects.count(), theme_count - 1)

        event = self._get_test_object_event()
        self.assertEqual(event, None)

    def test_theme_edit_view_no_permission(self):
        self._create_test_theme()

        theme_label = self.test_theme.label

        response = self._request_test_theme_edit_view()
        self.assertEqual(response.status_code, 404)

        self.test_theme.refresh_from_db()
        self.assertEqual(self.test_theme.label, theme_label)

        event = self._get_test_object_event()
        self.assertEqual(event.verb, event_theme_created.id)

    def test_theme_edit_view_with_access(self):
        self._create_test_theme()

        self.grant_access(
            obj=self.test_theme, permission=permission_theme_edit
        )

        theme_label = self.test_theme.label

        response = self._request_test_theme_edit_view()
        self.assertEqual(response.status_code, 302)

        self.test_theme.refresh_from_db()
        self.assertNotEqual(self.test_theme.label, theme_label)

        event = self._get_test_object_event()
        self.assertEqual(event.verb, event_theme_edited.id)

    def test_theme_list_view_with_no_permission(self):
        self._create_test_theme()

        response = self._request_test_theme_list_view()
        self.assertNotContains(
            response=response, text=self.test_theme.label, status_code=200
        )

        event = self._get_test_object_event()
        self.assertEqual(event.verb, event_theme_created.id)

    def test_theme_list_view_with_access(self):
        self._create_test_theme()

        self.grant_access(obj=self.test_theme, permission=permission_theme_view)

        response = self._request_test_theme_list_view()
        self.assertContains(
            response=response, text=self.test_theme.label, status_code=200
        )

        event = self._get_test_object_event()
        self.assertEqual(event.verb, event_theme_created.id)
