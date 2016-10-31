from __future__ import unicode_literals

from common.tests.test_views import GenericViewTestCase

from user_management.tests.literals import (
    TEST_USER_PASSWORD, TEST_USER_USERNAME
)

from ..classes import Statistic
from ..permissions import permission_statistics_view


class StatisticsViewTestCase(GenericViewTestCase):
    def test_statistic_detail_view_no_permissions(self):
        self.login(username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)

        statistic = Statistic.get_all()[0]

        response = self.get(
            'statistics:statistic_detail', args=(statistic.slug,)
        )

        self.assertEqual(response.status_code, 403)

    def test_statistic_detail_view_with_permissions(self):
        self.login(username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)

        self.role.permissions.add(permission_statistics_view.stored_permission)

        statistic = Statistic.get_all()[0]

        response = self.get(
            'statistics:statistic_detail', args=(statistic.slug,)
        )

        self.assertEqual(response.status_code, 200)

    def test_statistic_namespace_list_view_no_permissions(self):
        self.login(username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)

        response = self.get('statistics:namespace_list')

        self.assertEqual(response.status_code, 403)

    def test_statistic_namespace_list_view_with_permissions(self):
        self.login(username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)

        self.role.permissions.add(permission_statistics_view.stored_permission)

        response = self.get('statistics:namespace_list')

        self.assertEqual(response.status_code, 200)
