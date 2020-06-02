from django.urls import reverse

from mayan.apps.tests.tests.base import GenericViewTestCase

from ..links import (
    link_acl_delete, link_acl_list, link_acl_create, link_acl_permissions
)
from ..permissions import permission_acl_edit, permission_acl_view

from .mixins import ACLTestMixin


class ACLsLinksTestCase(ACLTestMixin, GenericViewTestCase):
    def setUp(self):
        super(ACLsLinksTestCase, self).setUp()
        self._setup_test_object()

    def test_object_acl_create_link(self):
        self.grant_access(
            obj=self.test_object, permission=permission_acl_edit
        )

        self.add_test_view(test_object=self.test_object)
        context = self.get_test_view()
        resolved_link = link_acl_create.resolve(context=context)

        self.assertNotEqual(resolved_link, None)

        self.assertEqual(
            resolved_link.url, reverse(
                viewname=link_acl_create.view,
                kwargs=self.test_content_object_view_kwargs
            )
        )

    def test_object_acl_delete_link(self):
        self._create_test_acl()

        self.grant_access(
            obj=self.test_object, permission=permission_acl_edit
        )

        self.add_test_view(test_object=self.test_acl)
        context = self.get_test_view()
        resolved_link = link_acl_delete.resolve(context=context)

        self.assertNotEqual(resolved_link, None)

        self.assertEqual(
            resolved_link.url, reverse(
                viewname=link_acl_delete.view, args=(self.test_acl.pk,)
            )
        )

    def test_object_acl_edit_link(self):
        self._create_test_acl()

        self.grant_access(
            obj=self.test_object, permission=permission_acl_edit
        )

        self.add_test_view(test_object=self.test_acl)
        context = self.get_test_view()
        resolved_link = link_acl_permissions.resolve(context=context)

        self.assertNotEqual(resolved_link, None)

        self.assertEqual(
            resolved_link.url, reverse(
                viewname=link_acl_permissions.view,
                args=(self.test_acl.pk,)
            )
        )

    def test_object_acl_list_link(self):
        self.grant_access(
            obj=self.test_object, permission=permission_acl_view
        )

        self.add_test_view(test_object=self.test_object)
        context = self.get_test_view()
        resolved_link = link_acl_list.resolve(context=context)
        self.assertNotEqual(resolved_link, None)

        self.assertEqual(
            resolved_link.url, reverse(
                viewname=link_acl_list.view,
                kwargs=self.test_content_object_view_kwargs
            )
        )
