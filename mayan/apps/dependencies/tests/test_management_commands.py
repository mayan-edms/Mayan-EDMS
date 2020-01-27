from __future__ import unicode_literals

from django.core import management
from django.utils.six import StringIO

import mayan

from mayan.apps.common.tests.base import BaseTestCase


class CommonManagementCommandTestCase(BaseTestCase):
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
