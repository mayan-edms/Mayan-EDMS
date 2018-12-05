from __future__ import absolute_import, unicode_literals

import os

from mayan.apps.common.settings import setting_paginate_by
from mayan.apps.common.tests import BaseTestCase

from .literals import ENVIRONMENT_TEST_NAME, ENVIRONMENT_TEST_VALUE


class ClassesTestCase(BaseTestCase):
    def test_environment_variable(self):
        os.environ[
            'MAYAN_{}'.format(ENVIRONMENT_TEST_NAME)
        ] = ENVIRONMENT_TEST_VALUE
        self.assertTrue(setting_paginate_by.value, ENVIRONMENT_TEST_VALUE)
