from mayan.apps.common.tests.base import BaseTestCase


class GroupEventsViewTestCase(BaseTestCase):
    def test_user_method_get_absolute_url(self):
        self._create_test_user()

        self.test_user.get_absolute_url()
