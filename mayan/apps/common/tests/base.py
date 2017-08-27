from __future__ import absolute_import, unicode_literals

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase

from django_downloadview import assert_download_response

from permissions.classes import Permission
from permissions.models import Role
from permissions.tests.literals import TEST_ROLE_LABEL
from smart_settings.classes import Namespace
from user_management.tests import (
    TEST_ADMIN_PASSWORD, TEST_ADMIN_USERNAME, TEST_ADMIN_EMAIL,
    TEST_GROUP_NAME, TEST_USER_EMAIL, TEST_USER_USERNAME, TEST_USER_PASSWORD
)

from .mixins import (
    ContentTypeCheckMixin, OpenFileCheckMixin, TempfileCheckMixin, UserMixin
)


class BaseTestCase(UserMixin, ContentTypeCheckMixin, OpenFileCheckMixin, TempfileCheckMixin, TestCase):
    """
    This is the most basic test case class any test in the project should use.
    """
    assert_download_response = assert_download_response

    def setUp(self):
        super(BaseTestCase, self).setUp()
        Namespace.invalidate_cache_all()
        Permission.invalidate_cache()
