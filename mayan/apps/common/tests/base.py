from __future__ import absolute_import, unicode_literals

from django.test import TestCase

from django_downloadview import assert_download_response

from mayan.apps.acls.tests.mixins import ACLTestCaseMixin
from mayan.apps.converter.tests.mixins import LayerTestCaseMixin
from mayan.apps.permissions.classes import Permission
from mayan.apps.smart_settings.classes import Namespace
from mayan.apps.user_management.tests.mixins import UserTestMixin

from .mixins import (
    ClientMethodsTestCaseMixin, ConnectionsCheckTestCaseMixin,
    ContentTypeCheckTestCaseMixin, ModelTestCaseMixin,
    OpenFileCheckTestCaseMixin, RandomPrimaryKeyModelMonkeyPatchMixin,
    SilenceLoggerTestCaseMixin, TempfileCheckTestCasekMixin,
    TestViewTestCaseMixin
)


class BaseTestCase(
    LayerTestCaseMixin, SilenceLoggerTestCaseMixin, ConnectionsCheckTestCaseMixin,
    RandomPrimaryKeyModelMonkeyPatchMixin, ACLTestCaseMixin,
    ModelTestCaseMixin, OpenFileCheckTestCaseMixin,
    TempfileCheckTestCasekMixin, UserTestMixin, TestCase
):
    """
    This is the most basic test case class any test in the project should use.
    """
    assert_download_response = assert_download_response

    def setUp(self):
        super(BaseTestCase, self).setUp()
        Namespace.invalidate_cache_all()
        Permission.invalidate_cache()


class GenericViewTestCase(
    ClientMethodsTestCaseMixin, ContentTypeCheckTestCaseMixin,
    TestViewTestCaseMixin, BaseTestCase
):
    """
    A generic view test case built on top of the base test case providing
    a single, user customizable view to test object resolution and shorthand
    HTTP method functions.
    """
