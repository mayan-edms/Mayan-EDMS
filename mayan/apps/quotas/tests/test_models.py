from mayan.apps.testing.tests.base import BaseTestCase

from .mixins import QuotaTestMixin


class QuotaModelTestCase(QuotaTestMixin, BaseTestCase):
    def test_method_get_absolute_url(self):
        self._create_test_quota()

        self.assertTrue(self.test_quota.get_absolute_url())
