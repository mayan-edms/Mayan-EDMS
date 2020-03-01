from __future__ import unicode_literals

from django.utils.encoding import force_text

from rest_framework import status

from mayan.apps.documents.permissions import permission_document_view
from mayan.apps.documents.tests.mixins import DocumentTestMixin
from mayan.apps.rest_api.tests.base import BaseAPITestCase

from ..models import Tag
from ..permissions import (
    permission_tag_attach, permission_tag_create, permission_tag_delete,
    permission_tag_edit, permission_tag_remove, permission_tag_view
)

from .mixins import (
    DocumentTagAPIViewTestMixin, TagAPIViewTestMixin,
    TagDocumentAPIViewTestMixin, TagTestMixin
)


class TagAPIViewTestCase(TagAPIViewTestMixin, TagTestMixin, BaseAPITestCase):
    def test_tag_create_api_view_no_permission(self):
        tag_count = Tag.objects.count()

        response = self._request_test_tag_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertEqual(Tag.objects.count(), tag_count)

    def test_tag_create_api_view_with_permission(self):
        self.grant_permission(permission=permission_tag_create)

        tag_count = Tag.objects.count()

        response = self._request_test_tag_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Tag.objects.count(), tag_count + 1)

    def test_tag_destroy_api_view_no_permission(self):
        self._create_test_tag()

        tag_count = Tag.objects.count()

        response = self._request_test_tag_destroy_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(Tag.objects.count(), tag_count)

    def test_tag_destroy_api_view_with_access(self):
        self._create_test_tag()

        self.grant_access(obj=self.test_tag, permission=permission_tag_delete)

        tag_count = Tag.objects.count()

        response = self._request_test_tag_destroy_api_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(Tag.objects.count(), tag_count - 1)

    def test_tag_list_api_view_no_permission(self):
        self._create_test_tag()
        response = self._request_test_tag_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

    def test_tag_list_api_view_with_access(self):
        self._create_test_tag()
        self.grant_access(
            obj=self.test_tag, permission=permission_tag_view
        )

        response = self._request_test_tag_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['results'][0]['label'],
            self.test_tag.label
        )

    def test_tag_partial_update_api_view_no_permission(self):
        self._create_test_tag()

        tag_label = self.test_tag.label
        tag_color = self.test_tag.color

        response = self._request_test_tag_edit_api_view(verb='patch')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_tag.refresh_from_db()
        self.assertEqual(self.test_tag.label, tag_label)
        self.assertEqual(self.test_tag.color, tag_color)

    def test_tag_partial_update_api_view_with_access(self):
        self._create_test_tag()

        self.grant_access(obj=self.test_tag, permission=permission_tag_edit)

        tag_label = self.test_tag.label
        tag_color = self.test_tag.color

        response = self._request_test_tag_edit_api_view(verb='patch')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_tag.refresh_from_db()
        self.assertNotEqual(self.test_tag.label, tag_label)
        self.assertNotEqual(self.test_tag.color, tag_color)

    def test_tag_retrive_api_view_no_permission(self):
        self._create_test_tag()

        response = self._request_test_tag_retrieve_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_tag_retrive_view_api_with_access(self):
        self._create_test_tag()
        self.grant_access(
            obj=self.test_tag, permission=permission_tag_view
        )

        response = self._request_test_tag_retrieve_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['label'], self.test_tag.label)

    def test_tag_update_api_view_no_permission(self):
        self._create_test_tag()

        tag_label = self.test_tag.label
        tag_color = self.test_tag.color

        response = self._request_test_tag_edit_api_view(verb='put')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_tag.refresh_from_db()
        self.assertEqual(self.test_tag.label, tag_label)
        self.assertEqual(self.test_tag.color, tag_color)

    def test_tag_update_api_view_with_access(self):
        self._create_test_tag()

        self.grant_access(obj=self.test_tag, permission=permission_tag_edit)

        tag_label = self.test_tag.label
        tag_color = self.test_tag.color

        response = self._request_test_tag_edit_api_view(verb='put')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_tag.refresh_from_db()
        self.assertNotEqual(self.test_tag.label, tag_label)
        self.assertNotEqual(self.test_tag.color, tag_color)


class TagDocumentAPIViewTestCase(
    DocumentTestMixin, TagDocumentAPIViewTestMixin, TagTestMixin,
    BaseAPITestCase
):
    def test_tag_document_attach_api_view_no_permission(self):
        self._create_test_tag()

        response = self._request_test_tag_document_attach_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertTrue(
            self.test_document not in self.test_tag.documents.all()
        )

    def test_tag_document_attach_api_view_with_tag_access(self):
        self._create_test_tag()

        self.grant_access(
            obj=self.test_tag, permission=permission_tag_attach
        )

        response = self._request_test_tag_document_attach_api_view()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertTrue(
            self.test_document not in self.test_tag.documents.all()
        )

    def test_tag_document_attach_api_view_with_document_access(self):
        self._create_test_tag()

        self.grant_access(
            obj=self.test_document, permission=permission_tag_attach
        )

        response = self._request_test_tag_document_attach_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertTrue(
            self.test_document not in self.test_tag.documents.all()
        )

    def test_tag_document_attach_api_view_with_full_access(self):
        self._create_test_tag()

        self.grant_access(
            obj=self.test_tag, permission=permission_tag_attach
        )
        self.grant_access(
            obj=self.test_document, permission=permission_tag_attach
        )

        response = self._request_test_tag_document_attach_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertTrue(self.test_document in self.test_tag.documents.all())

    def test_tag_document_list_api_view_no_permission(self):
        self._create_test_tag()
        self.test_tag.documents.add(self.test_document)

        response = self._request_test_tag_document_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_tag_document_list_api_view_with_tag_access(self):
        self._create_test_tag()
        self.test_tag.documents.add(self.test_document)

        self.grant_access(obj=self.test_tag, permission=permission_tag_view)

        response = self._request_test_tag_document_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['count'], 0)

    def test_tag_document_list_api_view_with_document_access(self):
        self._create_test_tag()
        self.test_tag.documents.add(self.test_document)

        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )
        response = self._request_test_tag_document_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_tag_document_list_api_view_with_access(self):
        self._create_test_tag()
        self.test_tag.documents.add(self.test_document)

        self.grant_access(obj=self.test_tag, permission=permission_tag_view)
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )
        response = self._request_test_tag_document_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.data['results'][0]['uuid'],
            force_text(self.test_document.uuid)
        )

    def test_tag_document_remove_api_view_no_permission(self):
        self._create_test_tag()
        self.test_tag.documents.add(self.test_document)

        response = self._request_test_tag_document_remove_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertTrue(
            self.test_document in self.test_tag.documents.all()
        )

    def test_tag_document_remove_api_view_with_tag_access(self):
        self._create_test_tag()
        self.test_tag.documents.add(self.test_document)

        self.grant_access(
            obj=self.test_tag, permission=permission_tag_remove
        )

        response = self._request_test_tag_document_remove_api_view()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertTrue(
            self.test_document in self.test_tag.documents.all()
        )

    def test_tag_document_remove_api_view_with_document_access(self):
        self._create_test_tag()
        self.test_tag.documents.add(self.test_document)

        self.grant_access(
            obj=self.test_document, permission=permission_tag_remove
        )

        response = self._request_test_tag_document_remove_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertTrue(
            self.test_document in self.test_tag.documents.all()
        )

    def test_tag_document_remove_api_view_with_full_access(self):
        self._create_test_tag()
        self.test_tag.documents.add(self.test_document)

        self.grant_access(
            obj=self.test_tag, permission=permission_tag_remove
        )
        self.grant_access(
            obj=self.test_document, permission=permission_tag_remove
        )

        response = self._request_test_tag_document_remove_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertTrue(
            self.test_document not in self.test_tag.documents.all()
        )


class DocumentTagAPIViewTestCase(
    DocumentTestMixin, DocumentTagAPIViewTestMixin, TagTestMixin, BaseAPITestCase
):
    def test_document_tag_attach_api_view_no_permission(self):
        self._create_test_tag()
        self.upload_document()

        response = self._request_test_document_tag_attach_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertTrue(self.test_tag not in self.test_document.tags.all())

    def test_document_tag_attach_api_view_with_document_access(self):
        self._create_test_tag()
        self.upload_document()

        self.grant_access(
            obj=self.test_document, permission=permission_tag_attach
        )

        response = self._request_test_document_tag_attach_api_view()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertTrue(self.test_tag not in self.test_document.tags.all())

    def test_document_tag_attach_api_view_with_tag_access(self):
        self._create_test_tag()
        self.upload_document()

        self.grant_access(
            obj=self.test_tag, permission=permission_tag_attach
        )

        response = self._request_test_document_tag_attach_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertTrue(self.test_tag not in self.test_document.tags.all())

    def test_document_tag_attach_api_view_with_full_access(self):
        self._create_test_tag()
        self.upload_document()

        self.grant_access(
            obj=self.test_document, permission=permission_tag_attach
        )
        self.grant_access(
            obj=self.test_tag, permission=permission_tag_attach
        )

        response = self._request_test_document_tag_attach_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertTrue(self.test_tag in self.test_document.tags.all())

    def test_document_tag_list_api_view_no_permission(self):
        self._create_test_tag()
        self.upload_document()
        self.test_tag.documents.add(self.test_document)

        response = self._request_test_document_tag_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_document_tag_list_api_view_with_document_access(self):
        self._create_test_tag()
        self.upload_document()
        self.test_tag.documents.add(self.test_document)

        self.grant_access(
            obj=self.test_document, permission=permission_tag_view
        )

        response = self._request_test_document_tag_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

    def test_document_tag_list_api_view_with_tag_access(self):
        self._create_test_tag()
        self.upload_document()
        self.test_tag.documents.add(self.test_document)

        self.grant_access(obj=self.test_tag, permission=permission_tag_view)

        response = self._request_test_document_tag_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_document_tag_list_api_view_with_full_access(self):
        self._create_test_tag()
        self.upload_document()
        self.test_tag.documents.add(self.test_document)

        self.grant_access(
            obj=self.test_document, permission=permission_tag_view
        )
        self.grant_access(obj=self.test_tag, permission=permission_tag_view)

        response = self._request_test_document_tag_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['label'], self.test_tag.label)

    def test_document_tag_remove_api_view_no_permission(self):
        self._create_test_tag()
        self.upload_document()
        self.test_tag.documents.add(self.test_document)

        response = self._request_test_document_tag_remove_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertTrue(self.test_tag in self.test_document.tags.all())

    def test_document_tag_remove_api_view_with_document_access(self):
        self._create_test_tag()
        self.upload_document()
        self.test_tag.documents.add(self.test_document)

        self.grant_access(
            obj=self.test_document, permission=permission_tag_remove
        )

        response = self._request_test_document_tag_remove_api_view()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertTrue(self.test_tag in self.test_document.tags.all())

    def test_document_tag_remove_api_view_with_tag_access(self):
        self._create_test_tag()
        self.upload_document()
        self.test_tag.documents.add(self.test_document)

        self.grant_access(obj=self.test_tag, permission=permission_tag_remove)

        response = self._request_test_document_tag_remove_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertTrue(self.test_tag in self.test_document.tags.all())

    def test_document_tag_remove_api_view_with_full_access(self):
        self._create_test_tag()
        self.upload_document()
        self.test_tag.documents.add(self.test_document)

        self.grant_access(
            obj=self.test_document, permission=permission_tag_remove
        )
        self.grant_access(obj=self.test_tag, permission=permission_tag_remove)

        response = self._request_test_document_tag_remove_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertFalse(self.test_tag in self.test_document.tags.all())
