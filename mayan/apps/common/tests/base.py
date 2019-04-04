from __future__ import absolute_import, unicode_literals

from django.test import TestCase

from django_downloadview import assert_download_response

from acls.tests.mixins import ACLTestCaseMixin
from permissions.classes import Permission
from smart_settings.classes import Namespace
from user_management.tests.mixins import UserTestCaseMixin

from .mixins import (
    ClientMethodsTestCaseMixin, ContentTypeCheckTestCaseMixin,
    DatabaseConversionMixin, OpenFileCheckTestCaseMixin,
    RandomPrimaryKeyModelMonkeyPatchMixin, TempfileCheckTestCasekMixin,
    TestViewTestCaseMixin
)


class BaseTestCase(RandomPrimaryKeyModelMonkeyPatchMixin, DatabaseConversionMixin, ACLTestCaseMixin, OpenFileCheckTestCaseMixin, TempfileCheckTestCasekMixin, TestCase):
    """
    This is the most basic test case class any test in the project should use.
    """
    assert_download_response = assert_download_response

    def setUp(self):
        super(BaseTestCase, self).setUp()
        Namespace.invalidate_cache_all()
        Permission.invalidate_cache()


class GenericViewTestCase(ClientMethodsTestCaseMixin, ContentTypeCheckTestCaseMixin, TestViewTestCaseMixin, UserTestCaseMixin, BaseTestCase):
    """
    A generic view test case built on top of the base test case providing
    a single, user customizable view to test object resolution and shorthand
    HTTP method functions.
    """
