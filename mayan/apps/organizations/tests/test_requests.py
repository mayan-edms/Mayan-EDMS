from django.test import override_settings

from mayan.apps.testing.tests.base import GenericViewTestCase
from mayan.apps.views.http import URL


TEST_INSTALLATION_SCHEME = 'https'
TEST_INSTALLATION_NETLOC = 'example.com:9999'

TEST_INSTALLATION_URL = URL(
    netloc=TEST_INSTALLATION_NETLOC, scheme=TEST_INSTALLATION_SCHEME
).to_string()


class RequestTestCase(GenericViewTestCase):
    @override_settings(ORGANIZATIONS_INSTALLATION_URL=TEST_INSTALLATION_URL)
    def test_installation_url_override(self):
        self.add_test_view()
        context = self.get_test_view()

        absolute_url = context['request'].build_absolute_uri()

        url = URL(url=absolute_url)

        self.assertEqual(url._split_result.netloc, TEST_INSTALLATION_NETLOC)
        self.assertEqual(url._split_result.scheme, TEST_INSTALLATION_SCHEME)

    def test_original_absolute_uri(self):
        self.add_test_view()
        context = self.get_test_view()

        absolute_url = context['request'].build_absolute_uri()

        url = URL(url=absolute_url)

        self.assertNotEqual(url._split_result.netloc, TEST_INSTALLATION_NETLOC)
        self.assertNotEqual(url._split_result.scheme, TEST_INSTALLATION_SCHEME)
