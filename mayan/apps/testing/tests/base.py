from django.apps import apps
from django.test import TestCase, TransactionTestCase, tag

from django_test_migrations.contrib.unittest_case import MigratorTestCase

from mayan.apps.acls.tests.mixins import ACLTestCaseMixin
from mayan.apps.converter.tests.mixins import LayerTestCaseMixin
from mayan.apps.events.tests.mixins import EventTestCaseMixin
from mayan.apps.permissions.tests.mixins import PermissionTestCaseMixin
from mayan.apps.smart_settings.tests.mixins import SmartSettingsTestCaseMixin
from mayan.apps.user_management.tests.mixins import UserTestMixin

from ..literals import EXCLUDE_TEST_TAG

from .mixins import (
    ClientMethodsTestCaseMixin, ConnectionsCheckTestCaseMixin,
    ContentTypeCheckTestCaseMixin, DelayTestCaseMixin,
    DescriptorLeakCheckTestCaseMixin, DownloadTestCaseMixin,
    ModelTestCaseMixin, OpenFileCheckTestCaseMixin,
    RandomPrimaryKeyModelMonkeyPatchMixin, SilenceLoggerTestCaseMixin,
    TempfileCheckTestCasekMixin, TestModelTestCaseMixin,
    TestViewTestCaseMixin
)


class BaseTestCaseMixin(
    DelayTestCaseMixin, LayerTestCaseMixin, SilenceLoggerTestCaseMixin,
    ConnectionsCheckTestCaseMixin, DownloadTestCaseMixin, EventTestCaseMixin,
    RandomPrimaryKeyModelMonkeyPatchMixin, ACLTestCaseMixin,
    ModelTestCaseMixin, OpenFileCheckTestCaseMixin,
    DescriptorLeakCheckTestCaseMixin, PermissionTestCaseMixin,
    SmartSettingsTestCaseMixin, TempfileCheckTestCasekMixin, UserTestMixin,
    TestModelTestCaseMixin
):
    """
    This is the most basic test case mixin class any test in the project
    should use.
    TestModelTestCaseMixin must go before TestViewTestCaseMixin to allow
    the test object to be available when the test view is prepared.

    Favor `OpenFileCheckTestCaseMixin` over
    `DescriptorLeakCheckTestCaseMixin` as it provides more context.
    """
    _skip_file_descriptor_test = True
    _skip_open_file_leak_test = True


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


class GenericTransactionViewTestCase(
    ClientMethodsTestCaseMixin, ContentTypeCheckTestCaseMixin,
    TestViewTestCaseMixin, BaseTransactionTestCase
):
    """
    A generic view test case built on top of the transaction base test case
    providing a single, user customizable view to test object resolution
    and shorthand HTTP method functions.
    """


@tag(EXCLUDE_TEST_TAG,)
class MayanMigratorTestCase(MigratorTestCase):
    def tearDown(self):
        ContentType = apps.get_model(
            app_label='contenttypes', model_name='ContentType'
        )

        ContentType.objects.clear_cache()

        super().tearDown()
