import mock

import mayan

from mayan.apps.tests.tests.base import BaseTestCase

from ..utils import PyPIClient


class PyPIClientTestCase(BaseTestCase):
    @mock.patch('mayan.apps.dependencies.utils.PyPIClient.get_versions', autospec=True)
    def test_check_version_not_latest_version(self, mock_package_releases):
        mock_package_releases.return_value = ('0.0.0',)
        with self.assertRaises(expected_exception=PyPIClient.NotLatestVersion):
            PyPIClient().check_version()

    @mock.patch('mayan.apps.dependencies.utils.PyPIClient.get_versions', autospec=True)
    def test_check_version_unknown_version(self, mock_package_releases):
        mock_package_releases.return_value = None
        with self.assertRaises(expected_exception=PyPIClient.UnknownLatestVersion):
            PyPIClient().check_version()

    @mock.patch('mayan.apps.dependencies.utils.PyPIClient.get_versions', autospec=True)
    def test_check_version_correct_version(self, mock_package_releases):
        mock_package_releases.return_value = (mayan.__version__,)
        PyPIClient().check_version()
