from mayan.apps.testing.tests.base import GenericViewTestCase

from ..dashboards import dashboard_administrator

from .mixins import DashboardViewTestMixin


class DashboardViewTestCase(DashboardViewTestMixin, GenericViewTestCase):
    test_dashboard = dashboard_administrator

    def test_dashboard_detail_view(self):
        self._clear_events()

        response = self._request_test_dashboard_detail_view()
        self.assertEqual(response.status_code, 200)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_dashboard_list_view(self):
        self._clear_events()

        response = self._request_test_dashboard_list_view()
        self.assertContains(
            response=response, status_code=200,
            text=self.test_dashboard.label
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
