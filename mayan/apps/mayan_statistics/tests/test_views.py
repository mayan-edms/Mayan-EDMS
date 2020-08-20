from mayan.apps.testing.tests.base import GenericViewTestCase

from ..classes import Statistic
from ..permissions import permission_statistics_view

from .mixins import StatisticsViewTestMixin


class StatisticsViewTestCase(StatisticsViewTestMixin, GenericViewTestCase):
    def test_statistic_detail_view_no_permission(self):
        self.statistic = Statistic.get_all()[0]

        response = self._request_test_statistic_detail_view()
        self.assertEqual(response.status_code, 403)

    def test_statistic_detail_view_with_permissions(self):
        self.grant_permission(permission=permission_statistics_view)

        self.statistic = Statistic.get_all()[0]

        response = self._request_test_statistic_detail_view()
        self.assertEqual(response.status_code, 200)

    def test_statistic_namespace_list_view_no_permission(self):
        response = self._request_test_namespace_list_view()
        self.assertEqual(response.status_code, 403)

    def test_statistic_namespace_list_view_with_permissions(self):
        self.grant_permission(permission=permission_statistics_view)

        response = self._request_test_namespace_list_view()
        self.assertEqual(response.status_code, 200)
