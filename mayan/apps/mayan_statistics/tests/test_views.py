from __future__ import unicode_literals

from mayan.apps.common.tests.base import GenericViewTestCase

from ..classes import Statistic
from ..permissions import permission_statistics_view


class StatisticsViewTestCase(GenericViewTestCase):
    def _request_test_statistic_detail_view(self):
        return self.get(
            viewname='statistics:statistic_detail', kwargs={
                'slug': self.statistic.slug
            }
        )

    def test_statistic_detail_view_no_permissions(self):
        self.statistic = Statistic.get_all()[0]

        response = self._request_test_statistic_detail_view()
        self.assertEqual(response.status_code, 403)

    def test_statistic_detail_view_with_permissions(self):
        self.grant_permission(permission=permission_statistics_view)

        self.statistic = Statistic.get_all()[0]

        response = self._request_test_statistic_detail_view()
        self.assertEqual(response.status_code, 200)

    def _request_test_namespace_list_view(self):
        return self.get(viewname='statistics:namespace_list')

    def test_statistic_namespace_list_view_no_permissions(self):
        response = self._request_test_namespace_list_view()
        self.assertEqual(response.status_code, 403)

    def test_statistic_namespace_list_view_with_permissions(self):
        self.grant_permission(permission=permission_statistics_view)

        response = self._request_test_namespace_list_view()
        self.assertEqual(response.status_code, 200)
