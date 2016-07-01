from __future__ import unicode_literals

import unittest

from django.apps import apps
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import connections, router
from django.http import HttpRequest
from django.test import TestCase, modify_settings, override_settings

from ..middleware import CurrentOrganizationMiddleware
from ..models import Organization
from ..shortcuts import get_current_organization
from ..utils import create_default_organization

TEST_ORGANIZATION_LABEL = 'Test organization label'


class OrganizationsFrameworkTests(TestCase):

    def setUp(self):
        Organization(
            id=settings.ORGANIZATION_ID, label=TEST_ORGANIZATION_LABEL
        ).save()

    def test_organization_manager(self):
        # Make sure that get_current() does not return a deleted Organization
        # object.
        s = Organization.objects.get_current()
        self.assertTrue(isinstance(s, Organization))
        s.delete()
        self.assertRaises(ObjectDoesNotExist, Organization.objects.get_current)

    def test_organization_cache(self):
        # After updating a Organization object (e.g. via the admin), we
        # shouldn't return a bogus value from the ORGANIZATION_CACHE.
        organization = Organization.objects.get_current()
        self.assertEqual(TEST_ORGANIZATION_LABEL, organization.label)
        s2 = Organization.objects.get(id=settings.ORGANIZATION_ID)
        s2.label = 'Example organization'
        s2.save()
        organization = Organization.objects.get_current()
        self.assertEqual('Example organization', organization.label)

    def test_delete_all_organizations_clears_cache(self):
        # When all organization objects are deleted the cache should also
        # be cleared and get_current() should raise a DoesNotExist.
        self.assertIsInstance(Organization.objects.get_current(), Organization)
        Organization.objects.all().delete()
        self.assertRaises(
            Organization.DoesNotExist, Organization.objects.get_current
        )

    @override_settings(ALLOWED_HOSTS=['example.com'])
    def test_get_current_organization(self):
        # Test that the correct Organization object is returned
        request = HttpRequest()
        request.META = {
            "SERVER_NAME": "example.com",
            "SERVER_PORT": "80",
        }
        organization = get_current_organization()
        self.assertTrue(isinstance(organization, Organization))
        self.assertEqual(organization.id, settings.ORGANIZATION_ID)

        # Test that an exception is raised if the organizations framework is
        # installed but there is no matching Organization
        organization.delete()
        self.assertRaises(
            ObjectDoesNotExist, get_current_organization, request
        )

        # A RequestOrganization is returned if the organizations framework is
        # not installed
        with self.modify_settings(INSTALLED_APPS={'remove': 'django.contrib.organizations'}):
            organization = get_current_organization(request)
            self.assertTrue(isinstance(organization, RequestOrganization))
            self.assertEqual(organization.name, "example.com")


class JustOtherRouter(object):
    def allow_migrate(self, db, model):
        return db == 'other'


@modify_settings(INSTALLED_APPS={'append': 'django.contrib.organizations'})
class CreateDefaultOrganizationTests(TestCase):
    multi_db = True

    def setUp(self):
        self.app_config = apps.get_app_config('organizations')
        # Delete the organization created as part of the default migration process.
        Organization.objects.all().delete()

    def test_basic(self):
        """
        #15346, #15573 - create_default_organization() creates an example organization only if
        none exist.
        """
        create_default_organization(self.app_config, verbosity=0)
        self.assertEqual(Organization.objects.count(), 1)

        create_default_organization(self.app_config, verbosity=0)
        self.assertEqual(Organization.objects.count(), 1)

    @unittest.skipIf('other' not in connections, "Requires 'other' database connection.")
    def test_multi_db_with_router(self):
        """
        #16353, #16828 - The default organization creation should respect db routing.
        """
        old_routers = router.routers
        router.routers = [JustOtherRouter()]
        try:
            create_default_organization(self.app_config, using='default', verbosity=0)
            create_default_organization(self.app_config, using='other', verbosity=0)
            self.assertFalse(Organization.objects.using('default').exists())
            self.assertTrue(Organization.objects.using('other').exists())
        finally:
            router.routers = old_routers

    @unittest.skipIf('other' not in connections, "Requires 'other' database connection.")
    def test_multi_db(self):
        create_default_organization(self.app_config, using='default', verbosity=0)
        create_default_organization(self.app_config, using='other', verbosity=0)
        self.assertTrue(Organization.objects.using('default').exists())
        self.assertTrue(Organization.objects.using('other').exists())

    def test_save_another(self):
        """
        #17415 - Another organization can be created right after the default one.

        On some backends the sequence needs to be reset after saving with an
        explicit ID. Test that there isn't a sequence collisions by saving
        another organization. This test is only meaningful with databases that use
        sequences for automatic primary keys such as PostgreSQL and Oracle.
        """
        create_default_organization(self.app_config, verbosity=0)
        Organization(domain='example2.com', name='example2.com').save()


class MiddlewareTest(TestCase):

    def test_request(self):
        """ Makes sure that the request has correct `organization` attribute. """
        middleware = CurrentOrganizationMiddleware()
        request = HttpRequest()
        middleware.process_request(request)
        self.assertEqual(request.organization.id, settings.ORGANIZATION_ID)
