import mock

from django.core import management
from django.utils.six import StringIO

import mayan

from mayan.apps.common.tests.base import BaseTestCase

from ..utils import (
    MESSAGE_NOT_LATEST, MESSAGE_UNKNOWN_VERSION, MESSAGE_UP_TO_DATE
)


class ShowVersionManagementCommandTestCase(BaseTestCase):
    create_test_case_user = False

    def test_version_command_base(self):
        out = StringIO()
        management.call_command(command_name='showversion', stdout=out)
        self.assertIn(mayan.__version__, out.getvalue())

    def test_version_command_build_string(self):
        out = StringIO()
        management.call_command(
            command_name='showversion', build_string=True, stdout=out
        )
        self.assertIn(mayan.__build_string__, out.getvalue())


class CheckVersionManagementCommandTestCase(BaseTestCase):
    def _call_command(self):
        out = StringIO()
        management.call_command(
            command_name='checkversion', stdout=out
        )
        return out.getvalue()

    @mock.patch('mayan.apps.dependencies.utils.PyPIClient.get_versions', autospec=True)
    def test_check_version_not_latest_version(self, mock_package_releases):
        mock_package_releases.return_value = ('0.0.0',)
        text = self._call_command()
        self.assertTrue(text.startswith(MESSAGE_NOT_LATEST[:-2]))

    @mock.patch('mayan.apps.dependencies.utils.PyPIClient.get_versions', autospec=True)
    def test_check_version_unknown_version(self, mock_package_releases):
        mock_package_releases.return_value = None
        text = self._call_command()
        self.assertTrue(text.startswith(MESSAGE_UNKNOWN_VERSION))

    @mock.patch('mayan.apps.dependencies.utils.PyPIClient.get_versions', autospec=True)
    def test_check_version_correct_version(self, mock_package_releases):
        mock_package_releases.return_value = (mayan.__version__,)
        text = self._call_command()
        self.assertTrue(text.startswith(MESSAGE_UP_TO_DATE))
