from __future__ import absolute_import, unicode_literals

from django.core.urlresolvers import reverse
from django.template import Context

from acls.models import AccessControlList
from common.tests.literals import TEST_VIEW_NAME
from common.tests.test_views import GenericViewTestCase
from permissions import Permission, PermissionNamespace
from user_management.tests import TEST_USER_PASSWORD, TEST_USER_USERNAME

from ..classes import Link

TEST_PERMISSION_NAMESPACE_NAME = 'test namespace name'
TEST_PERMISSION_NAMESPACE_TEXT = 'test namespace text'
TEST_PERMISSION_NAME = 'test permission name'
TEST_PERMISSION_LABEL = 'test permission label'
TEST_LINK_TEXT = 'test link text'


class LinkClassTestCase(GenericViewTestCase):
    def setUp(self):
        super(LinkClassTestCase, self).setUp()

        self.add_test_view(test_object=self.group)

        self.namespace = PermissionNamespace(
            TEST_PERMISSION_NAMESPACE_NAME, TEST_PERMISSION_NAMESPACE_TEXT
        )

        self.permission = self.namespace.add_permission(
            name=TEST_PERMISSION_NAME, label=TEST_PERMISSION_LABEL
        )

        self.link = Link(text=TEST_LINK_TEXT, view=TEST_VIEW_NAME)
        Permission.invalidate_cache()

    def test_link_resolve(self):
        response = self.get(TEST_VIEW_NAME)
        context = Context({'request': response.wsgi_request})

        resolved_link = self.link.resolve(context=context)

        self.assertEqual(resolved_link.url, reverse(TEST_VIEW_NAME))

    def test_link_permission_resolve_no_permission(self):
        self.login(
            username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD
        )

        link = Link(
            permissions=(self.permission,), text=TEST_LINK_TEXT,
            view=TEST_VIEW_NAME
        )

        response = self.get(TEST_VIEW_NAME)
        response.context.update({'request': response.wsgi_request})
        context = Context(response.context)

        resolved_link = link.resolve(context=context)

        self.assertEqual(resolved_link, None)

    def test_link_permission_resolve_with_permission(self):
        self.login(
            username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD
        )

        link = Link(
            permissions=(self.permission,), text=TEST_LINK_TEXT,
            view=TEST_VIEW_NAME
        )

        self.role.permissions.add(self.permission.stored_permission)

        response = self.get(TEST_VIEW_NAME)
        response.context.update({'request': response.wsgi_request})
        context = Context(response.context)

        resolved_link = link.resolve(context=context)

        self.assertEqual(resolved_link.url, reverse(TEST_VIEW_NAME))

    def test_link_permission_resolve_with_acl(self):
        # ACL is tested agains the resolved_object or just {{ object }} if not
        self.login(
            username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD
        )

        link = Link(
            permissions=(self.permission,), text=TEST_LINK_TEXT,
            view=TEST_VIEW_NAME
        )

        acl = AccessControlList.objects.create(
            content_object=self.group, role=self.role
        )
        acl.permissions.add(self.permission.stored_permission)

        response = self.get(TEST_VIEW_NAME)
        response.context.update({'request': response.wsgi_request})
        context = Context(response.context)

        resolved_link = link.resolve(context=context)

        self.assertNotEqual(resolved_link, None)
        self.assertEqual(resolved_link.url, reverse(TEST_VIEW_NAME))
