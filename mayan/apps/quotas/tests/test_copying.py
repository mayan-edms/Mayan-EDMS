from mayan.apps.common.tests.mixins import ObjectCopyTestMixin
from mayan.apps.testing.tests.base import BaseTestCase

from .mixins import QuotaTestMixin


class QuotaCopyTestCase(
    QuotaTestMixin, ObjectCopyTestMixin, BaseTestCase
):
    def setUp(self):
        super().setUp()
        self._create_test_quota_with_mixins()
        self._test_object = self._test_quota
