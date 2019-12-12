from __future__ import absolute_import, unicode_literals

from django.test import TestCase

from mayan.apps.acls.tests.mixins import ACLTestCaseMixin
from mayan.apps.converter.tests.mixins import LayerTestCaseMixin
from mayan.apps.permissions.tests.mixins import PermissionTestCaseMixin
from mayan.apps.smart_settings.tests.mixins import SmartSettingsTestCaseMixin


from mayan.apps.user_management.tests.mixins import UserTestMixin

from .mixins import (
    ClientMethodsTestCaseMixin, ConnectionsCheckTestCaseMixin,
    ContentTypeCheckTestCaseMixin, DownloadTestCaseMixin, ModelTestCaseMixin,
    OpenFileCheckTestCaseMixin, RandomPrimaryKeyModelMonkeyPatchMixin,
    SilenceLoggerTestCaseMixin, TempfileCheckTestCasekMixin,
    TestViewTestCaseMixin
)


class BaseTestCase(
    LayerTestCaseMixin, SilenceLoggerTestCaseMixin,
    ConnectionsCheckTestCaseMixin, DownloadTestCaseMixin,
    RandomPrimaryKeyModelMonkeyPatchMixin, ACLTestCaseMixin,
    ModelTestCaseMixin, OpenFileCheckTestCaseMixin, PermissionTestCaseMixin,
    SmartSettingsTestCaseMixin, TempfileCheckTestCasekMixin, UserTestMixin,
    TestCase
):
    """
    This is the most basic test case class any test in the project should use.
    """


class GenericViewTestCase(
    ClientMethodsTestCaseMixin, ContentTypeCheckTestCaseMixin,
    TestViewTestCaseMixin, BaseTestCase
):
    """
    A generic view test case built on top of the base test case providing
    a single, user customizable view to test object resolution and shorthand
    HTTP method functions.
    """
