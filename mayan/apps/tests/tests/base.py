from django.test import TestCase, TransactionTestCase

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


class BaseTestCaseMixin(
    LayerTestCaseMixin, SilenceLoggerTestCaseMixin,
    ConnectionsCheckTestCaseMixin, DownloadTestCaseMixin,
    RandomPrimaryKeyModelMonkeyPatchMixin, ACLTestCaseMixin,
    ModelTestCaseMixin, OpenFileCheckTestCaseMixin, PermissionTestCaseMixin,
    SmartSettingsTestCaseMixin, TempfileCheckTestCasekMixin, UserTestMixin,
):
    """
    This is the most basic test case mixin class any test in the project
    should use.
    """


class BaseTestCase(BaseTestCaseMixin, TestCase):
    """
    All the project test mixin on top of Django test case class.
    """


class BaseTransactionTestCase(BaseTestCaseMixin, TransactionTestCase):
    """
    All the project test mixin on top of Django transaction test case class.
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
