from __future__ import absolute_import, unicode_literals

from documents.tests.test_views import GenericDocumentViewTestCase
from user_management.tests import (
    TEST_USER_USERNAME, TEST_USER_PASSWORD
)

from ..models import SmartLink
from ..permissions import (
    permission_smart_link_create, permission_smart_link_delete,
    permission_smart_link_edit
)

TEST_SMART_LINK_LABEL = 'test label'
TEST_SMART_LINK_EDITED_LABEL = 'test edited label'


class SmartLinkViewTestCase(GenericDocumentViewTestCase):
    def test_smart_link_create_view_no_permission(self):
        self.login(username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)

        response = self.post(
            'linking:smart_link_create', data={
                'label': TEST_SMART_LINK_LABEL
            }
        )

        self.assertEquals(response.status_code, 403)
        self.assertEqual(SmartLink.objects.count(), 0)

    def test_smart_link_create_view_with_permission(self):
        self.login(username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)

        self.role.permissions.add(
            permission_smart_link_create.stored_permission
        )

        response = self.post(
            'linking:smart_link_create', data={
                'label': TEST_SMART_LINK_LABEL
            }, follow=True
        )
        self.assertContains(response, text='created', status_code=200)
        self.assertEqual(SmartLink.objects.count(), 1)
        self.assertEqual(
            SmartLink.objects.first().label, TEST_SMART_LINK_LABEL
        )

    def test_smart_link_delete_view_no_permission(self):
        self.login(username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)

        smart_link = SmartLink.objects.create(label=TEST_SMART_LINK_LABEL)

        response = self.post(
            'linking:smart_link_delete', args=(smart_link.pk,)
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(SmartLink.objects.count(), 1)

    def test_smart_link_delete_view_with_permission(self):
        self.login(username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)

        self.role.permissions.add(
            permission_smart_link_delete.stored_permission
        )

        smart_link = SmartLink.objects.create(label=TEST_SMART_LINK_LABEL)

        response = self.post(
            'linking:smart_link_delete', args=(smart_link.pk,), follow=True
        )

        self.assertContains(response, text='deleted', status_code=200)
        self.assertEqual(SmartLink.objects.count(), 0)

    def test_smart_link_edit_view_no_permission(self):
        self.login(username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)

        smart_link = SmartLink.objects.create(label=TEST_SMART_LINK_LABEL)

        response = self.post(
            'linking:smart_link_edit', args=(smart_link.pk,), data={
                'label': TEST_SMART_LINK_EDITED_LABEL
            }
        )
        self.assertEqual(response.status_code, 403)
        smart_link = SmartLink.objects.get(pk=smart_link.pk)
        self.assertEqual(smart_link.label, TEST_SMART_LINK_LABEL)

    def test_smart_link_edit_view_with_permission(self):
        self.login(username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)

        self.role.permissions.add(
            permission_smart_link_edit.stored_permission
        )

        smart_link = SmartLink.objects.create(label=TEST_SMART_LINK_LABEL)

        response = self.post(
            'linking:smart_link_edit', args=(smart_link.pk,), data={
                'label': TEST_SMART_LINK_EDITED_LABEL
            }, follow=True
        )

        smart_link = SmartLink.objects.get(pk=smart_link.pk)
        self.assertContains(response, text='update', status_code=200)
        self.assertEqual(smart_link.label, TEST_SMART_LINK_EDITED_LABEL)
