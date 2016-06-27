from __future__ import unicode_literals

from django.test import TestCase

from .mixins import FileDescriptorCheckMixin, TempfileCheckMixin


class BaseTestCase(FileDescriptorCheckMixin, TempfileCheckMixin, TestCase):
    """
    This is the most basic test case class any test in the project should use.
    """
