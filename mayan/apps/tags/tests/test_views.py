from __future__ import unicode_literals

from documents.permissions import permission_document_view
from documents.tests.test_views import GenericDocumentViewTestCase
from user_management.tests import TEST_USER_PASSWORD, TEST_USER_USERNAME

from ..models import Tag
from ..permissions import (
    permission_tag_attach, permission_tag_create, permission_tag_delete,
    permission_tag_edit, permission_tag_remove, permission_tag_view
)

from .literals import (
    TEST_TAG_COLOR, TEST_TAG_COLOR_EDITED, TEST_TAG_LABEL,
    TEST_TAG_LABEL_EDITED
)


class TagViewTestCase(GenericDocumentViewTestCase):
    def setUp(self):
        super(TagViewTestCase, self).setUp()

        self.tag = Tag.objects.create(
            color=TEST_TAG_COLOR, label=TEST_TAG_LABEL
        )

    def tearDown(self):
        super(TagViewTestCase, self).tearDown()
        if self.tag.pk:
            self.tag.delete()

    def test_tag_create_view_no_permissions(self):
        self.login(username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)

        self.tag.delete()
        self.assertEqual(Tag.objects.count(), 0)

        response = self.post(
            'tags:tag_create', data={
                'label': TEST_TAG_LABEL,
                'color': TEST_TAG_COLOR
            }
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(Tag.objects.count(), 0)

    def test_tag_create_view_with_permissions(self):
        self.login(username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)

        self.tag.delete()
        self.assertEqual(Tag.objects.count(), 0)

        self.role.permissions.add(permission_tag_create.stored_permission)

        response = self.post(
            'tags:tag_create', data={
                'label': TEST_TAG_LABEL,
                'color': TEST_TAG_COLOR
            }, follow=True
        )

        self.assertContains(response, text='created', status_code=200)

        self.assertEqual(Tag.objects.count(), 1)
        tag = Tag.objects.first()
        self.assertEqual(tag.label, TEST_TAG_LABEL)
        self.assertEqual(tag.color, TEST_TAG_COLOR)

    def test_tag_delete_view_no_permissions(self):
        self.login(username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)

        self.assertEqual(Tag.objects.count(), 1)

        response = self.post(
            'tags:tag_delete', args=(self.tag.pk,)
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Tag.objects.count(), 1)

    def test_tag_delete_view_with_permissions(self):
        self.login(username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)

        self.assertEqual(Tag.objects.count(), 1)

        self.role.permissions.add(permission_tag_delete.stored_permission)

        response = self.post(
            'tags:tag_delete', args=(self.tag.pk,), follow=True
        )

        self.assertContains(response, text='deleted', status_code=200)

        self.assertEqual(Tag.objects.count(), 0)

    def test_tag_multiple_delete_view_no_permissions(self):
        self.login(username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)

        self.assertEqual(Tag.objects.count(), 1)

        response = self.post(
            'tags:tag_multiple_delete', data={'id_list': self.tag.pk}
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Tag.objects.count(), 1)

    def test_tag_multiple_delete_view_with_permissions(self):
        self.login(username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)

        self.assertEqual(Tag.objects.count(), 1)

        self.role.permissions.add(permission_tag_delete.stored_permission)

        response = self.post(
            'tags:tag_multiple_delete', data={'id_list': self.tag.pk},
            follow=True
        )

        self.assertContains(response, text='deleted', status_code=200)

        self.assertEqual(Tag.objects.count(), 0)

    def test_tag_edit_view_no_permissions(self):
        self.login(username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)

        response = self.post(
            'tags:tag_edit', args=(self.tag.pk,), data={
                'label': TEST_TAG_LABEL_EDITED, 'color': TEST_TAG_COLOR_EDITED
            }
        )

        self.assertEqual(response.status_code, 403)
        tag = Tag.objects.get(pk=self.tag.pk)
        self.assertEqual(tag.label, TEST_TAG_LABEL)
        self.assertEqual(tag.color, TEST_TAG_COLOR)

    def test_tag_edit_view_with_permissions(self):
        self.login(username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)

        self.role.permissions.add(permission_tag_edit.stored_permission)

        response = self.post(
            'tags:tag_edit', args=(self.tag.pk,), data={
                'label': TEST_TAG_LABEL_EDITED, 'color': TEST_TAG_COLOR_EDITED
            }, follow=True
        )

        self.assertContains(response, text='saved', status_code=200)
        tag = Tag.objects.get(pk=self.tag.pk)
        self.assertEqual(tag.label, TEST_TAG_LABEL_EDITED)
        self.assertEqual(tag.color, TEST_TAG_COLOR_EDITED)

    def test_document_tags_widget_no_permissions(self):
        self.login(username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)

        self.tag.documents.add(self.document)
        response = self.get('documents:document_list')
        self.assertNotContains(response, text=TEST_TAG_LABEL, status_code=200)

    def test_document_tags_widget_with_permissions(self):
        self.login(username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)

        self.tag.documents.add(self.document)
        self.role.permissions.add(permission_tag_view.stored_permission)
        self.role.permissions.add(permission_document_view.stored_permission)
        response = self.get('documents:document_list')

        self.assertContains(response, text=TEST_TAG_LABEL, status_code=200)

    def test_document_attach_tag_view_no_permission(self):
        self.login(username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)

        self.assertEqual(self.document.tags.count(), 0)

        self.role.permissions.add(permission_tag_view.stored_permission)
        response = self.post(
            'tags:tag_attach', args=(self.document.pk,), data={
                'tag': self.tag.pk,
                'user': self.user.pk
            }
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(self.document.tags.count(), 0)

    def test_document_attach_tag_view_with_permission(self):
        self.login(username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)

        self.assertEqual(self.document.tags.count(), 0)

        self.role.permissions.add(permission_tag_attach.stored_permission)
        # permission_tag_view is needed because the form filters the
        # choices
        self.role.permissions.add(permission_tag_view.stored_permission)

        response = self.post(
            'tags:tag_attach', args=(self.document.pk,), data={
                'tag': self.tag.pk,
                'user': self.user.pk
            }, follow=True
        )

        self.assertEqual(response.status_code, 200)

        self.assertQuerysetEqual(
            self.document.tags.all(), (repr(self.tag),)
        )

    def test_document_multiple_attach_tag_view_no_permission(self):
        self.login(username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)

        self.assertEqual(self.document.tags.count(), 0)
        self.role.permissions.add(permission_tag_view.stored_permission)

        response = self.post(
            'tags:multiple_documents_tag_attach', data={
                'id_list': self.document.pk, 'tag': self.tag.pk,
                'user': self.user.pk
            }
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.document.tags.count(), 0)

    def test_document_multiple_attach_tag_view_with_permission(self):
        self.login(username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)

        self.assertEqual(self.document.tags.count(), 0)

        self.role.permissions.add(permission_tag_attach.stored_permission)

        # permission_tag_view is needed because the form filters the
        # choices
        self.role.permissions.add(permission_tag_view.stored_permission)

        response = self.post(
            'tags:multiple_documents_tag_attach', data={
                'id_list': self.document.pk, 'tag': self.tag.pk,
                'user': self.user.pk
            }, follow=True
        )

        self.assertEqual(response.status_code, 200)

        self.assertQuerysetEqual(
            self.document.tags.all(), (repr(self.tag),)
        )

    def test_single_document_multiple_tag_remove_view_no_permissions(self):
        self.login(username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)

        self.document.tags.add(self.tag)
        self.assertQuerysetEqual(self.document.tags.all(), (repr(self.tag),))
        self.role.permissions.add(permission_tag_view.stored_permission)

        response = self.post(
            'tags:single_document_multiple_tag_remove',
            args=(self.document.pk,), data={
                'id_list': self.tag.pk,
            }
        )

        self.assertEqual(response.status_code, 302)
        self.assertQuerysetEqual(self.document.tags.all(), (repr(self.tag),))

    def test_single_document_multiple_tag_remove_view_with_permission(self):
        self.login(username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)

        self.document.tags.add(self.tag)
        self.assertQuerysetEqual(self.document.tags.all(), (repr(self.tag),))

        self.role.permissions.add(permission_tag_remove.stored_permission)
        self.role.permissions.add(permission_tag_view.stored_permission)

        response = self.post(
            'tags:single_document_multiple_tag_remove',
            args=(self.document.pk,), data={
                'id_list': self.tag.pk,
            }, follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.document.tags.count(), 0)

    def test_multiple_documents_selection_tag_remove_view_no_permissions(self):
        self.login(username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)

        self.document.tags.add(self.tag)
        self.assertQuerysetEqual(self.document.tags.all(), (repr(self.tag),))
        self.role.permissions.add(permission_tag_view.stored_permission)

        response = self.post(
            'tags:multiple_documents_selection_tag_remove',
            data={
                'id_list': self.document.pk,
                'tag': self.tag.pk,
            }
        )

        self.assertEqual(response.status_code, 302)
        self.assertQuerysetEqual(self.document.tags.all(), (repr(self.tag),))

    def test_multiple_documents_selection_tag_remove_view_with_permission(self):
        self.login(username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)

        self.document.tags.add(self.tag)
        self.assertQuerysetEqual(self.document.tags.all(), (repr(self.tag),))

        self.role.permissions.add(permission_tag_remove.stored_permission)
        self.role.permissions.add(permission_tag_view.stored_permission)

        response = self.post(
            'tags:multiple_documents_selection_tag_remove',
            data={
                'id_list': self.document.pk,
                'tag': self.tag.pk,
            }, follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.document.tags.count(), 0)
