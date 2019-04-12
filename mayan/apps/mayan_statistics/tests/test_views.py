from __future__ import unicode_literals

from mayan.apps.common.tests import GenericViewTestCase

from ..classes import Statistic
from ..permissions import permission_statistics_view


class StatisticsViewTestCase(GenericViewTestCase):
    def setUp(self):
        super(StatisticsViewTestCase, self).setUp()
        self.login_user()

    def test_statistic_detail_view_no_permissions(self):
        statistic = Statistic.get_all()[0]

        response = self.get(
            'statistics:statistic_detail', args=(statistic.slug,)
        )

        self.assertEqual(response.status_code, 403)

    def test_statistic_detail_view_with_permissions(self):
        self.grant_permission(permission=permission_statistics_view)

        statistic = Statistic.get_all()[0]

        response = self.get(
            'statistics:statistic_detail', args=(statistic.slug,)
        )

        self.assertEqual(response.status_code, 200)

    def test_statistic_namespace_list_view_no_permissions(self):
        response = self.get('statistics:namespace_list')

        self.assertEqual(response.status_code, 403)

    def test_statistic_namespace_list_view_with_permissions(self):
        self.grant_permission(permission=permission_statistics_view)

        response = self.get('statistics:namespace_list')

        self.assertEqual(response.status_code, 200)
