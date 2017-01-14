from __future__ import absolute_import, unicode_literals

from django.test import TestCase

from permissions.classes import Permission
from smart_settings.classes import Namespace

from .mixins import (
    ContentTypeCheckMixin, OpenFileCheckMixin, TempfileCheckMixin
)


class BaseTestCase(ContentTypeCheckMixin, OpenFileCheckMixin, TempfileCheckMixin, TestCase):
    """
    This is the most basic test case class any test in the project should use.
    """

    def setUp(self):
        super(BaseTestCase, self).setUp()
        Namespace.invalidate_cache_all()
        Permission.invalidate_cache()
