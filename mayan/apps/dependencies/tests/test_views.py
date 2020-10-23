import mock

import mayan

from mayan.apps.testing.tests.base import GenericViewTestCase

from ..utils import (
    MESSAGE_NOT_LATEST, MESSAGE_UNKNOWN_VERSION, MESSAGE_UP_TO_DATE
)

from .mixins import CheckVersionViewTestMixin


class CheckVersionViewTestCase(CheckVersionViewTestMixin, GenericViewTestCase):
    @mock.patch('mayan.apps.dependencies.utils.PyPIClient.get_versions', autospec=True)
    def test_check_version_not_latest_version(self, mock_package_releases):
        mock_package_releases.return_value = ('0.0.0',)
        response = self._request_check_version_view()
        self.assertContains(
            response=response, text=MESSAGE_NOT_LATEST[:-2], status_code=200
        )

    @mock.patch('mayan.apps.dependencies.utils.PyPIClient.get_versions', autospec=True)
    def test_check_version_unknown_version(self, mock_package_releases):
        mock_package_releases.return_value = None
        response = self._request_check_version_view()
        self.assertContains(
            response=response, text=MESSAGE_UNKNOWN_VERSION, status_code=200
        )

    @mock.patch('mayan.apps.dependencies.utils.PyPIClient.get_versions', autospec=True)
    def test_check_version_correct_version(self, mock_package_releases):
        mock_package_releases.return_value = (mayan.__version__,)
        response = self._request_check_version_view()
        self.assertContains(
            response=response, text=MESSAGE_UP_TO_DATE, status_code=200
        )
