from __future__ import unicode_literals

from common.tests import BaseTestCase

from ..models import Organization
from ..utils import create_default_organization


class OrganizationTestCase(BaseTestCase):
    def setUp(self):
        create_default_organization()

    def tearDown(self):
        Organization.objects.all().delete()
        Organization.objects.clear_cache()
