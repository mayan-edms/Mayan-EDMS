from __future__ import unicode_literals

from django.test import override_settings
from django.utils.encoding import force_text

from rest_framework import status

from documents.permissions import permission_document_view
from documents.tests import DocumentTestMixin
from rest_api.tests import BaseAPITestCase

from ..models import Tag
from ..permissions import (
    permission_tag_attach, permission_tag_create, permission_tag_delete,
    permission_tag_edit, permission_tag_remove, permission_tag_view
)

from .literals import (
    TEST_TAG_COLOR, TEST_TAG_COLOR_EDITED, TEST_TAG_LABEL,
    TEST_TAG_LABEL_EDITED
)


@override_settings(OCR_AUTO_OCR=False)
class TagAPITestCase(DocumentTestMixin, BaseAPITestCase):
    auto_upload_document = False

    def setUp(self):
        super(TagAPITestCase, self).setUp()
        self.login_user()

    def _create_tag(self):
        return Tag.objects.create(
            color=TEST_TAG_COLOR, label=TEST_TAG_LABEL
        )

    def _request_tag_create_view(self):
        return self.post(
            viewname='rest_api:tag-list', data={
                'label': TEST_TAG_LABEL, 'color': TEST_TAG_COLOR
            }
        )

    def test_tag_create_view_no_permission(self):
        response = self._request_tag_create_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Tag.objects.count(), 0)

    def test_tag_create_view_with_permission(self):
        self.grant_permission(permission=permission_tag_create)
        response = self._request_tag_create_view()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        tag = Tag.objects.first()
        self.assertEqual(response.data['id'], tag.pk)
        self.assertEqual(response.data['label'], TEST_TAG_LABEL)
        self.assertEqual(response.data['color'], TEST_TAG_COLOR)

        self.assertEqual(Tag.objects.count(), 1)
        self.assertEqual(tag.label, TEST_TAG_LABEL)
        self.assertEqual(tag.color, TEST_TAG_COLOR)

    def _request_tag_delete_view(self):
        return self.delete(
            viewname='rest_api:tag-detail', args=(self.tag.pk,)
        )

    def test_tag_delete_view_no_access(self):
        self.tag = self._create_tag()
        response = self._request_tag_delete_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(self.tag in Tag.objects.all())

    def test_tag_delete_view_with_access(self):
        self.tag = self._create_tag()
        self.grant_access(permission=permission_tag_delete, obj=self.tag)
        response = self._request_tag_delete_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(self.tag in Tag.objects.all())

    def _request_tag_document_list_view(self):
        return self.get(
            viewname='rest_api:tag-document-list', args=(self.tag.pk,)
        )

    def test_tag_document_list_view_no_access(self):
        self.tag = self._create_tag()
        self.document = self.upload_document()
        self.tag.documents.add(self.document)
        response = self._request_tag_document_list_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_tag_document_list_view_with_tag_access(self):
        self.tag = self._create_tag()
        self.document = self.upload_document()
        self.tag.documents.add(self.document)
        self.grant_access(permission=permission_tag_view, obj=self.tag)
        response = self._request_tag_document_list_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

    def test_tag_document_list_view_with_document_access(self):
        self.tag = self._create_tag()
        self.document = self.upload_document()
        self.tag.documents.add(self.document)
        self.grant_access(
            permission=permission_document_view, obj=self.document
        )
        response = self._request_tag_document_list_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_tag_document_list_view_with_access(self):
        self.tag = self._create_tag()
        self.document = self.upload_document()
        self.tag.documents.add(self.document)
        self.grant_access(permission=permission_tag_view, obj=self.tag)
        self.grant_access(
            permission=permission_document_view, obj=self.document
        )
        response = self._request_tag_document_list_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['results'][0]['uuid'],
            force_text(self.document.uuid)
        )

    def _request_tag_edit_via_patch_view(self):
        return self.patch(
            viewname='rest_api:tag-detail', args=(self.tag.pk,), data={
                'label': TEST_TAG_LABEL_EDITED,
                'color': TEST_TAG_COLOR_EDITED
            }
        )

    def test_tag_edit_via_patch_no_access(self):
        self.tag = self._create_tag()
        response = self._request_tag_edit_via_patch_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.tag.refresh_from_db()
        self.assertEqual(self.tag.label, TEST_TAG_LABEL)
        self.assertEqual(self.tag.color, TEST_TAG_COLOR)

    def test_tag_edit_via_patch_with_access(self):
        self.tag = self._create_tag()
        self.grant_access(permission=permission_tag_edit, obj=self.tag)
        response = self._request_tag_edit_via_patch_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.tag.refresh_from_db()
        self.assertEqual(self.tag.label, TEST_TAG_LABEL_EDITED)
        self.assertEqual(self.tag.color, TEST_TAG_COLOR_EDITED)

    def _request_tag_edit_via_put_view(self):
        return self.put(
            viewname='rest_api:tag-detail', args=(self.tag.pk,), data={
                'label': TEST_TAG_LABEL_EDITED,
                'color': TEST_TAG_COLOR_EDITED
            }
        )

    def test_tag_edit_via_put_no_access(self):
        self.tag = self._create_tag()
        response = self._request_tag_edit_via_put_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.tag.refresh_from_db()
        self.assertEqual(self.tag.label, TEST_TAG_LABEL)
        self.assertEqual(self.tag.color, TEST_TAG_COLOR)

    def test_tag_edit_via_put_with_access(self):
        self.tag = self._create_tag()
        self.grant_access(permission=permission_tag_edit, obj=self.tag)
        response = self._request_tag_edit_via_put_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.tag.refresh_from_db()
        self.assertEqual(self.tag.label, TEST_TAG_LABEL_EDITED)
        self.assertEqual(self.tag.color, TEST_TAG_COLOR_EDITED)

    def _request_document_attach_tag_view(self):
        return self.post(
            viewname='rest_api:document-tag-list', args=(self.document.pk,),
            data={'tag_pk': self.tag.pk}
        )

    def test_document_attach_tag_view_no_access(self):
        self.tag = self._create_tag()
        self.document = self.upload_document()
        response = self._request_document_attach_tag_view()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertFalse(self.tag in self.document.tags.all())

    def test_document_attach_tag_view_with_document_access(self):
        self.tag = self._create_tag()
        self.document = self.upload_document()
        self.grant_access(permission=permission_tag_attach, obj=self.document)
        response = self._request_document_attach_tag_view()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertFalse(self.tag in self.document.tags.all())

    def test_document_attach_tag_view_with_tag_access(self):
        self.tag = self._create_tag()
        self.document = self.upload_document()
        self.grant_access(permission=permission_tag_attach, obj=self.tag)
        response = self._request_document_attach_tag_view()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(self.tag in self.document.tags.all())

    def test_document_attach_tag_view_with_access(self):
        self.tag = self._create_tag()
        self.document = self.upload_document()
        self.grant_access(permission=permission_tag_attach, obj=self.document)
        self.grant_access(permission=permission_tag_attach, obj=self.tag)
        response = self._request_document_attach_tag_view()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(self.tag in self.document.tags.all())

    def _request_document_tag_detail_view(self):
        return self.get(
            viewname='rest_api:document-tag-detail', args=(
                self.document.pk, self.tag.pk
            )
        )

    def test_document_tag_detail_view_no_access(self):
        self.tag = self._create_tag()
        self.document = self.upload_document()
        self.tag.documents.add(self.document)
        response = self._request_document_tag_detail_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_document_tag_detail_view_with_document_access(self):
        self.tag = self._create_tag()
        self.document = self.upload_document()
        self.tag.documents.add(self.document)
        self.grant_access(permission=permission_document_view, obj=self.document)
        response = self._request_document_tag_detail_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_document_tag_detail_view_with_tag_access(self):
        self.tag = self._create_tag()
        self.document = self.upload_document()
        self.tag.documents.add(self.document)
        self.grant_access(permission=permission_tag_view, obj=self.tag)
        response = self._request_document_tag_detail_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_document_tag_detail_view_with_access(self):
        self.tag = self._create_tag()
        self.document = self.upload_document()
        self.tag.documents.add(self.document)
        self.grant_access(permission=permission_tag_view, obj=self.tag)
        self.grant_access(permission=permission_document_view, obj=self.document)
        response = self._request_document_tag_detail_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['label'], self.tag.label)

    def _request_document_tag_list_view(self):
        return self.get(
            viewname='rest_api:document-tag-list', args=(self.document.pk,)
        )

    def test_document_tag_list_view_no_access(self):
        self.tag = self._create_tag()
        self.document = self.upload_document()
        self.tag.documents.add(self.document)
        response = self._request_document_tag_list_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_document_tag_list_view_with_document_access(self):
        self.tag = self._create_tag()
        self.document = self.upload_document()
        self.tag.documents.add(self.document)
        self.grant_access(permission=permission_document_view, obj=self.document)
        response = self._request_document_tag_list_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

    def test_document_tag_list_view_with_tag_access(self):
        self.tag = self._create_tag()
        self.document = self.upload_document()
        self.tag.documents.add(self.document)
        self.grant_access(permission=permission_tag_view, obj=self.tag)
        response = self._request_document_tag_list_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_document_tag_list_view_with_access(self):
        self.tag = self._create_tag()
        self.document = self.upload_document()
        self.tag.documents.add(self.document)
        self.grant_access(permission=permission_document_view, obj=self.document)
        self.grant_access(permission=permission_tag_view, obj=self.tag)
        response = self._request_document_tag_list_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['label'], self.tag.label)

    def _request_document_tag_remove_view(self):
        return self.delete(
            viewname='rest_api:document-tag-detail', args=(
                self.document.pk, self.tag.pk
            )
        )

    def test_document_tag_remove_view_no_access(self):
        self.tag = self._create_tag()
        self.document = self.upload_document()
        self.tag.documents.add(self.document)
        response = self._request_document_tag_remove_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(self.tag in self.document.tags.all())

    def test_document_tag_remove_view_with_document_access(self):
        self.tag = self._create_tag()
        self.document = self.upload_document()
        self.tag.documents.add(self.document)
        self.grant_access(permission=permission_tag_remove, obj=self.document)
        response = self._request_document_tag_remove_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(self.tag in self.document.tags.all())

    def test_document_tag_remove_view_with_tag_access(self):
        self.tag = self._create_tag()
        self.document = self.upload_document()
        self.tag.documents.add(self.document)
        self.grant_access(permission=permission_tag_remove, obj=self.tag)
        response = self._request_document_tag_remove_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(self.tag in self.document.tags.all())

    def test_document_tag_remove_view_with_access(self):
        self.tag = self._create_tag()
        self.document = self.upload_document()
        self.tag.documents.add(self.document)
        self.grant_access(permission=permission_document_view, obj=self.document)
        self.grant_access(permission=permission_tag_remove, obj=self.tag)
        response = self._request_document_tag_remove_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(self.tag in self.document.tags.all())
