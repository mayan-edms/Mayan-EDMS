import time

from django.utils.encoding import force_text

from rest_framework import status

from mayan.apps.rest_api.tests.base import BaseAPITestCase

from ..models import Document, DocumentType
from ..permissions import (
    permission_document_create, permission_document_download,
    permission_document_delete, permission_document_edit,
    permission_document_new_version, permission_document_properties_edit,
    permission_document_restore, permission_document_trash,
    permission_document_view, permission_document_type_create,
    permission_document_type_delete, permission_document_type_edit,
    permission_document_version_revert, permission_document_version_view
)

from .literals import (
    TEST_DOCUMENT_DESCRIPTION_EDITED, TEST_PDF_DOCUMENT_FILENAME,
    TEST_DOCUMENT_PATH, TEST_DOCUMENT_TYPE_LABEL, TEST_DOCUMENT_TYPE_2_LABEL,
    TEST_DOCUMENT_TYPE_LABEL_EDITED, TEST_DOCUMENT_VERSION_COMMENT_EDITED,
    TEST_SMALL_DOCUMENT_FILENAME
)
from .mixins import DocumentTestMixin, DocumentVersionTestMixin


class DocumentTypeAPIViewTestMixin:
    def _request_test_document_type_api_create_view(self):
        return self.post(
            viewname='rest_api:documenttype-list', data={
                'label': TEST_DOCUMENT_TYPE_LABEL
            }
        )

    def _request_test_document_type_api_delete_view(self):
        return self.delete(
            viewname='rest_api:documenttype-detail', kwargs={
                'pk': self.test_document_type.pk,
            }
        )

    def _request_test_document_type_api_patch_view(self):
        return self.patch(
            viewname='rest_api:documenttype-detail', kwargs={
                'pk': self.test_document_type.pk,
            }, data={'label': TEST_DOCUMENT_TYPE_LABEL_EDITED}
        )

    def _request_test_document_type_api_put_view(self):
        return self.put(
            viewname='rest_api:documenttype-detail', kwargs={
                'pk': self.test_document_type.pk,
            }, data={'label': TEST_DOCUMENT_TYPE_LABEL_EDITED}
        )


class DocumentTypeAPIViewTestCase(
    DocumentTypeAPIViewTestMixin, DocumentTestMixin, BaseAPITestCase
):
    auto_upload_test_document = False
    auto_create_test_document_type = False

    def test_document_type_api_create_view_no_permission(self):
        response = self._request_test_document_type_api_create_view()

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(DocumentType.objects.all().count(), 0)

    def test_document_type_api_create_view_with_permission(self):
        self.grant_permission(permission=permission_document_type_create)

        response = self._request_test_document_type_api_create_view()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(DocumentType.objects.all().count(), 1)
        self.assertEqual(
            DocumentType.objects.all().first().label, TEST_DOCUMENT_TYPE_LABEL
        )

    def test_document_type_api_delete_view_no_permission(self):
        self.test_document_type = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE_LABEL
        )

        response = self._request_test_document_type_api_delete_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_document_type_api_delete_view_with_access(self):
        self.test_document_type = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE_LABEL
        )
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_delete
        )

        response = self._request_test_document_type_api_delete_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(DocumentType.objects.all().count(), 0)

    def test_document_type_api_edit_via_patch_view_no_permission(self):
        self.test_document_type = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE_LABEL
        )

        response = self._request_test_document_type_api_patch_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_document_type_api_edit_via_patch_view_with_access(self):
        self.test_document_type = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE_LABEL
        )
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )

        response = self._request_test_document_type_api_put_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_document_type.refresh_from_db()
        self.assertEqual(
            self.test_document_type.label, TEST_DOCUMENT_TYPE_LABEL_EDITED
        )

    def test_document_type_api_edit_via_put_view_no_permission(self):
        self._create_test_document_type()

        response = self._request_test_document_type_api_put_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_document_type_api_edit_via_put_view_with_access(self):
        self.test_document_type = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE_LABEL
        )
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )

        response = self._request_test_document_type_api_put_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_document_type.refresh_from_db()
        self.assertEqual(
            self.test_document_type.label, TEST_DOCUMENT_TYPE_LABEL_EDITED
        )


class DocumentAPIViewTestMixin:
    def _request_test_document_api_download_view(self):
        return self.get(
            viewname='rest_api:document-download', kwargs={
                'pk': self.test_document.pk
            }
        )

    def _request_test_document_api_upload_view(self):
        with open(file=TEST_DOCUMENT_PATH, mode='rb') as file_object:
            return self.post(
                viewname='rest_api:document-list', data={
                    'document_type': self.test_document_type.pk,
                    'file': file_object
                }
            )

    def _request_test_document_description_api_edit_via_patch_view(self):
        return self.patch(
            viewname='rest_api:document-detail', kwargs={
                'pk': self.test_document.pk
            }, data={'description': TEST_DOCUMENT_DESCRIPTION_EDITED}
        )

    def _request_test_document_description_api_edit_via_put_view(self):
        return self.put(
            viewname='rest_api:document-detail', kwargs={
                'pk': self.test_document.pk
            }, data={'description': TEST_DOCUMENT_DESCRIPTION_EDITED}
        )

    def _request_test_document_document_type_change_api_view(self):
        return self.post(
            viewname='rest_api:document-type-change', kwargs={
                'pk': self.test_document.pk
            }, data={'new_document_type': self.test_document_type_2.pk}
        )


class DocumentAPIViewTestCase(
    DocumentAPIViewTestMixin, DocumentTestMixin, BaseAPITestCase
):
    auto_upload_test_document = False

    def test_document_api_download_view_no_permission(self):
        self._upload_test_document()

        response = self._request_test_document_api_download_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_document_api_download_view_with_access(self):
        self._upload_test_document()
        self.grant_access(
            obj=self.test_document, permission=permission_document_download
        )

        response = self._request_test_document_api_download_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        with self.test_document.open() as file_object:
            self.assert_download_response(
                response=response, content=file_object.read(),
                filename=TEST_SMALL_DOCUMENT_FILENAME,
                mime_type=self.test_document.file_mimetype
            )

    def test_document_api_upload_view_no_permission(self):
        response = self._request_test_document_api_upload_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_document_api_upload_view_with_access(self):
        self.grant_access(
            obj=self.test_document_type, permission=permission_document_create
        )

        response = self._request_test_document_api_upload_view()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Document.objects.count(), 1)

        document = Document.objects.first()

        # Correct document PK
        self.assertEqual(document.pk, response.data['id'])

        # Document initial version uploaded correctly
        self.assertEqual(document.versions.count(), 1)

        # Document's file exists in the document storage
        self.assertEqual(document.exists(), True)

        # And is of the expected size
        self.assertEqual(document.size, 272213)

        # Correct mimetype
        self.assertEqual(document.file_mimetype, 'application/pdf')

        # Check document file encoding
        self.assertEqual(document.file_mime_encoding, 'binary')
        self.assertEqual(document.label, TEST_PDF_DOCUMENT_FILENAME)
        self.assertEqual(
            document.checksum,
            'c637ffab6b8bb026ed3784afdb07663fddc60099853fae2be93890852a69ecf3'
        )
        self.assertEqual(document.page_count, 47)

    def test_document_document_type_change_api_via_no_permission(self):
        self._upload_test_document()
        self.test_document_type_2 = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE_2_LABEL
        )

        response = self._request_test_document_document_type_change_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_document.refresh_from_db()
        self.assertEqual(
            self.test_document.document_type,
            self.test_document_type
        )

    def test_document_document_type_change_api_via_with_access(self):
        self._upload_test_document()
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_properties_edit
        )
        self.test_document_type_2 = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE_2_LABEL
        )

        response = self._request_test_document_document_type_change_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_document.refresh_from_db()
        self.assertEqual(
            self.test_document.document_type,
            self.test_document_type_2
        )

    def test_document_description_api_edit_via_patch_view_no_permission(self):
        self._upload_test_document()

        response = self._request_test_document_description_api_edit_via_patch_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_document_description_api_edit_via_patch_view_with_access(self):
        self._upload_test_document()
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_properties_edit
        )

        response = self._request_test_document_description_api_edit_via_patch_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_document.refresh_from_db()
        self.assertEqual(
            self.test_document.description,
            TEST_DOCUMENT_DESCRIPTION_EDITED
        )

    def test_document_description_api_edit_via_put_view_no_permission(self):
        self._upload_test_document()

        response = self._request_test_document_description_api_edit_via_put_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_document_description_api_edit_via_put_view_with_access(self):
        self._upload_test_document()
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_properties_edit
        )

        response = self._request_test_document_description_api_edit_via_put_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_document.refresh_from_db()
        self.assertEqual(
            self.test_document.description,
            TEST_DOCUMENT_DESCRIPTION_EDITED
        )


class DocumentVersionAPIViewTestMixin:
    def _request_test_document_version_api_download_view(self):
        return self.get(
            viewname='rest_api:documentversion-download', kwargs={
                'pk': self.test_document.pk,
                'version_pk': self.test_document.latest_version.pk,
            }
        )

    def _request_test_document_version_api_edit_via_patch_view(self):
        return self.patch(
            viewname='rest_api:documentversion-detail', kwargs={
                'pk': self.test_document.pk,
                'version_pk': self.test_document.latest_version.pk
            }, data={'comment': TEST_DOCUMENT_VERSION_COMMENT_EDITED}
        )

    def _request_test_document_version_api_edit_via_put_view(self):
        return self.put(
            viewname='rest_api:documentversion-detail', kwargs={
                'pk': self.test_document.pk,
                'version_pk': self.test_document.latest_version.pk
            }, data={'comment': TEST_DOCUMENT_VERSION_COMMENT_EDITED}
        )

    def _request_test_document_version_api_list_view(self):
        return self.get(
            viewname='rest_api:document-version-list', kwargs={
                'pk': self.test_document.pk
            }
        )

    def _request_test_document_version_api_revert_view(self):
        return self.delete(
            viewname='rest_api:documentversion-detail', kwargs={
                'pk': self.test_document.pk,
                'version_pk': self.test_document.latest_version.pk
            }
        )

    def _request_test_document_version_api_upload_view(self):
        # Artificial delay since MySQL doesn't store microsecond data in
        # timestamps. Version timestamp is used to determine which version
        # is the latest.
        time.sleep(1)

        with open(file=TEST_DOCUMENT_PATH, mode='rb') as file_descriptor:
            return self.post(
                viewname='rest_api:document-version-list', kwargs={
                    'pk': self.test_document.pk,
                }, data={
                    'comment': '', 'file': file_descriptor,
                }
            )


class DocumentVersionAPIViewTestCase(
    DocumentVersionAPIViewTestMixin, DocumentTestMixin,
    DocumentVersionTestMixin, BaseAPITestCase
):
    auto_upload_test_document = False

    def test_document_version_api_download_view_no_permission(self):
        self._upload_test_document()

        response = self._request_test_document_version_api_download_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_document_version_api_download_view_with_access(self):
        self._upload_test_document()
        self.grant_access(
            obj=self.test_document, permission=permission_document_download
        )

        response = self._request_test_document_version_api_download_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        with self.test_document.latest_version.open() as file_object:
            self.assert_download_response(
                response=response, content=file_object.read(),
                filename=force_text(self.test_document.latest_version),
                mime_type=self.test_document.file_mimetype
            )

    def test_document_version_api_download_preserve_extension_view(self):
        self._upload_test_document()
        self.grant_access(
            obj=self.test_document, permission=permission_document_download
        )

        response = self.get(
            viewname='rest_api:documentversion-download', kwargs={
                'pk': self.test_document.pk,
                'version_pk': self.test_document.latest_version.pk,
            }, data={'preserve_extension': True}
        )

        with self.test_document.latest_version.open() as file_object:
            self.assert_download_response(
                response=response, content=file_object.read(),
                filename=self.test_document.latest_version.get_rendered_string(
                    preserve_extension=True
                ), mime_type=self.test_document.file_mimetype
            )

    def test_document_version_api_list_view_no_permission(self):
        self._upload_test_document()
        self._upload_new_version()

        response = self._request_test_document_version_api_list_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['count'], 0)

    def test_document_version_api_list_view_with_access(self):
        self._upload_test_document()
        self._upload_new_version()

        self.grant_access(
            obj=self.test_document, permission=permission_document_version_view
        )
        response = self._request_test_document_version_api_list_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.data['results'][1]['checksum'],
            self.test_document.latest_version.checksum
        )

    def test_document_version_api_edit_via_patch_view_no_permission(self):
        self._upload_test_document()

        response = self._request_test_document_version_api_edit_via_patch_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_document_version_api_edit_via_patch_view_with_access(self):
        self._upload_test_document()
        self.grant_access(
            obj=self.test_document, permission=permission_document_edit
        )
        response = self._request_test_document_version_api_edit_via_patch_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.test_document.latest_version.refresh_from_db()
        self.assertEqual(self.test_document.versions.count(), 1)
        self.assertEqual(
            self.test_document.latest_version.comment,
            TEST_DOCUMENT_VERSION_COMMENT_EDITED
        )

    def test_document_version_api_edit_via_put_view_no_permission(self):
        self._upload_test_document()

        response = self._request_test_document_version_api_edit_via_put_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_document_version_api_edit_via_put_view_with_access(self):
        self._upload_test_document()
        self.grant_access(
            obj=self.test_document, permission=permission_document_edit
        )

        response = self._request_test_document_version_api_edit_via_put_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_document.latest_version.refresh_from_db()
        self.assertEqual(self.test_document.versions.count(), 1)
        self.assertEqual(
            self.test_document.latest_version.comment,
            TEST_DOCUMENT_VERSION_COMMENT_EDITED
        )

    def test_document_version_api_revert_view_no_permission(self):
        self._upload_test_document()
        self._upload_new_version()

        response = self._request_test_document_version_api_revert_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_document_version_api_revert_view_with_access(self):
        self._upload_test_document()
        self._upload_new_version()
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_version_revert
        )

        response = self._request_test_document_version_api_revert_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(self.test_document.versions.count(), 1)
        self.assertEqual(
            self.test_document.versions.first(), self.test_document.latest_version
        )

    def test_document_version_api_upload_view_no_permission(self):
        self._upload_test_document()

        response = self._request_test_document_version_api_upload_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_document_version_api_upload_view_with_access(self):
        self._upload_test_document()
        self.grant_access(
            obj=self.test_document, permission=permission_document_new_version
        )

        response = self._request_test_document_version_api_upload_view()
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

        self.assertEqual(self.test_document.versions.count(), 2)
        self.assertEqual(self.test_document.exists(), True)
        self.assertEqual(self.test_document.size, 272213)
        self.assertEqual(self.test_document.file_mimetype, 'application/pdf')
        self.assertEqual(self.test_document.file_mime_encoding, 'binary')
        self.assertEqual(
            self.test_document.checksum,
            'c637ffab6b8bb026ed3784afdb07663fddc60099853fae2be93890852a69ecf3'
        )
        self.assertEqual(self.test_document.page_count, 47)


class DocumentPageAPIViewTestMixin:
    def _request_document_page_image(self):
        page = self.test_document.pages.first()
        return self.get(
            viewname='rest_api:documentpage-image', kwargs={
                'pk': page.document.pk, 'version_pk': page.document_version.pk,
                'page_pk': page.pk
            }
        )


class DocumentPageAPIViewTestCase(
    DocumentPageAPIViewTestMixin, DocumentTestMixin, BaseAPITestCase
):
    def test_document_page_api_image_view_no_access(self):
        response = self._request_document_page_image()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_document_page_api_image_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        response = self._request_document_page_image()
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TrashedDocumentAPIViewTestMixin:
    def _request_test_document_api_trash_view(self):
        return self.delete(
            viewname='rest_api:document-detail', kwargs={
                'pk': self.test_document.pk
            }
        )

    def _request_test_trashed_document_api_delete_view(self):
        return self.delete(
            viewname='rest_api:trasheddocument-detail', kwargs={
                'pk': self.test_document.pk
            }
        )

    def _request_test_trashed_document_api_detail_view(self):
        return self.get(
            viewname='rest_api:trasheddocument-detail', kwargs={
                'pk': self.test_document.pk
            }
        )

    def _request_test_trashed_document_api_image_view(self):
        latest_version = self.test_document.latest_version

        return self.get(
            viewname='rest_api:documentpage-image', kwargs={
                'pk': latest_version.document.pk,
                'version_pk': latest_version.pk,
                'page_pk': latest_version.pages.first().pk
            }
        )

    def _request_test_trashed_document_api_list_view(self):
        return self.get(
            viewname='rest_api:trasheddocument-list'
        )

    def _request_test_trashed_document_api_restore_view(self):
        return self.post(
            viewname='rest_api:trasheddocument-restore', kwargs={
                'pk': self.test_document.pk
            }
        )


class TrashedDocumentAPIViewTestCase(
    TrashedDocumentAPIViewTestMixin, DocumentTestMixin, BaseAPITestCase
):
    auto_upload_test_document = False

    def test_document_api_trash_view_no_permission(self):
        self._upload_test_document()

        response = self._request_test_document_api_trash_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_document_api_trash_view_with_access(self):
        self._upload_test_document()
        self.grant_access(
            obj=self.test_document, permission=permission_document_trash
        )

        response = self._request_test_document_api_trash_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(Document.objects.count(), 0)
        self.assertEqual(Document.trash.count(), 1)

    def test_trashed_document_api_delete_view_no_access(self):
        self._upload_test_document()
        self.test_document.delete()

        response = self._request_test_trashed_document_api_delete_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(Document.objects.count(), 0)
        self.assertEqual(Document.trash.count(), 1)

    def test_trashed_document_api_delete_view_with_access(self):
        self._upload_test_document()
        self.test_document.delete()
        self.grant_access(
            obj=self.test_document, permission=permission_document_delete
        )

        response = self._request_test_trashed_document_api_delete_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(Document.objects.count(), 0)
        self.assertEqual(Document.trash.count(), 0)

    def test_trashed_document_api_detail_view_no_access(self):
        self._upload_test_document()
        self.test_document.delete()

        response = self._request_test_trashed_document_api_detail_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertFalse('uuid' in response.data)

    def test_trashed_document_api_detail_view_with_access(self):
        self._upload_test_document()
        self.test_document.delete()
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        response = self._request_test_trashed_document_api_detail_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['uuid'], force_text(self.test_document.uuid)
        )

    def test_trashed_document_api_image_view_no_permission(self):
        self._upload_test_document()
        self.test_document.delete()

        response = self._request_test_trashed_document_api_image_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_trashed_document_api_image_view_with_access(self):
        self._upload_test_document()
        self.test_document.delete()
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        response = self._request_test_trashed_document_api_image_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_trashed_document_api_list_view_no_access(self):
        self._upload_test_document()
        self.test_document.delete()

        response = self._request_test_trashed_document_api_list_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

    def test_trashed_document_api_list_view_with_access(self):
        self._upload_test_document()
        self.test_document.delete()
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        response = self._request_test_trashed_document_api_list_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['results'][0]['uuid'],
            force_text(self.test_document.uuid)
        )

    def test_trashed_document_api_restore_view_no_access(self):
        self._upload_test_document()
        self.test_document.delete()

        response = self._request_test_trashed_document_api_restore_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(Document.trash.count(), 1)
        self.assertEqual(Document.objects.count(), 0)

    def test_trashed_document_api_restore_view_with_access(self):
        self._upload_test_document()
        self.test_document.delete()

        self.grant_access(
            obj=self.test_document, permission=permission_document_restore
        )
        response = self._request_test_trashed_document_api_restore_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(Document.trash.count(), 0)
        self.assertEqual(Document.objects.count(), 1)
