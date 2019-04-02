# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import time

from django.test import override_settings
from django.utils.encoding import force_text

from django_downloadview import assert_download_response
from rest_framework import status

from rest_api.tests import BaseAPITestCase

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
    TEST_DOCUMENT_DESCRIPTION_EDITED, TEST_DOCUMENT_FILENAME,
    TEST_DOCUMENT_PATH, TEST_DOCUMENT_TYPE_LABEL,
    TEST_DOCUMENT_TYPE_LABEL_EDITED, TEST_DOCUMENT_VERSION_COMMENT_EDITED,
    TEST_SMALL_DOCUMENT_FILENAME
)
from .mixins import DocumentTestMixin


class DocumentTypeAPITestCase(BaseAPITestCase):
    def setUp(self):
        super(DocumentTypeAPITestCase, self).setUp()
        self.login_user()

    def _request_document_type_create(self):
        return self.post(
            viewname='rest_api:documenttype-list', data={
                'label': TEST_DOCUMENT_TYPE_LABEL
            }
        )

    def test_document_type_create_no_permission(self):
        response = self._request_document_type_create()

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(DocumentType.objects.all().count(), 0)

    def test_document_type_create_with_permission(self):
        self.grant_permission(permission=permission_document_type_create)

        response = self._request_document_type_create()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(DocumentType.objects.all().count(), 1)
        self.assertEqual(
            DocumentType.objects.all().first().label, TEST_DOCUMENT_TYPE_LABEL
        )

    def _request_document_type_patch(self):
        return self.patch(
            viewname='rest_api:documenttype-detail', args=(
                self.document_type.pk,
            ), data={'label': TEST_DOCUMENT_TYPE_LABEL_EDITED}
        )

    def test_document_type_edit_via_patch_no_permission(self):
        self.document_type = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE_LABEL
        )
        response = self._request_document_type_patch()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_document_type_edit_via_patch_with_access(self):
        self.document_type = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE_LABEL
        )
        self.grant_access(
            permission=permission_document_type_edit, obj=self.document_type
        )
        response = self._request_document_type_put()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.document_type.refresh_from_db()
        self.assertEqual(
            self.document_type.label, TEST_DOCUMENT_TYPE_LABEL_EDITED
        )

    def _request_document_type_put(self):
        return self.put(
            viewname='rest_api:documenttype-detail', args=(
                self.document_type.pk,
            ), data={'label': TEST_DOCUMENT_TYPE_LABEL_EDITED}
        )

    def test_document_type_edit_via_put_no_permission(self):
        self.document_type = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE_LABEL
        )
        response = self._request_document_type_put()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_document_type_edit_via_put_with_access(self):
        self.document_type = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE_LABEL
        )
        self.grant_access(
            permission=permission_document_type_edit, obj=self.document_type
        )
        response = self._request_document_type_put()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.document_type.refresh_from_db()
        self.assertEqual(
            self.document_type.label, TEST_DOCUMENT_TYPE_LABEL_EDITED
        )

    def _request_document_type_delete(self):
        return self.delete(
            viewname='rest_api:documenttype-detail', args=(
                self.document_type.pk,
            )
        )

    def test_document_type_delete_no_permission(self):
        self.document_type = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE_LABEL
        )

        response = self._request_document_type_delete()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_document_type_delete_with_access(self):
        self.expected_content_type = None
        self.document_type = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE_LABEL
        )
        self.grant_access(
            permission=permission_document_type_delete, obj=self.document_type
        )
        response = self._request_document_type_delete()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(DocumentType.objects.all().count(), 0)


@override_settings(OCR_AUTO_OCR=False)
class DocumentAPITestCase(DocumentTestMixin, BaseAPITestCase):
    auto_upload_document = False

    def setUp(self):
        super(DocumentAPITestCase, self).setUp()
        self.login_user()

    def _request_document_upload(self):
        with open(TEST_DOCUMENT_PATH, mode='rb') as file_descriptor:
            return self.post(
                viewname='rest_api:document-list', data={
                    'document_type': self.document_type.pk,
                    'file': file_descriptor
                }
            )

    def test_document_upload_no_permission(self):
        response = self._request_document_upload()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_document_upload_with_access(self):
        self.grant_access(
            permission=permission_document_create, obj=self.document_type
        )
        response = self._request_document_upload()
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
        self.assertEqual(document.label, TEST_DOCUMENT_FILENAME)
        self.assertEqual(
            document.checksum,
            'c637ffab6b8bb026ed3784afdb07663fddc60099853fae2be93890852a69ecf3'
        )
        self.assertEqual(document.page_count, 47)

    def _request_document_new_version_upload(self):
        # Artifical delay since MySQL doesn't store microsecond data in
        # timestamps. Version timestamp is used to determine which version
        # is the latest.
        time.sleep(1)

        with open(TEST_DOCUMENT_PATH, mode='rb') as file_descriptor:
            return self.post(
                viewname='rest_api:document-version-list', args=(
                    self.document.pk,
                ), data={
                    'comment': '', 'file': file_descriptor,
                }
            )

    def test_document_new_version_upload_no_permission(self):
        self.document = self.upload_document()
        response = self._request_document_new_version_upload()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_document_new_version_upload_with_access(self):
        self.document = self.upload_document()
        self.grant_access(
            permission=permission_document_new_version, obj=self.document
        )
        response = self._request_document_new_version_upload()
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

        self.assertEqual(self.document.versions.count(), 2)
        self.assertEqual(self.document.exists(), True)
        self.assertEqual(self.document.size, 272213)
        self.assertEqual(self.document.file_mimetype, 'application/pdf')
        self.assertEqual(self.document.file_mime_encoding, 'binary')
        self.assertEqual(
            self.document.checksum,
            'c637ffab6b8bb026ed3784afdb07663fddc60099853fae2be93890852a69ecf3'
        )
        self.assertEqual(self.document.page_count, 47)

    def _create_new_version(self):
        # Needed by MySQL as milliseconds value is not store in timestamp field
        time.sleep(1)

        with open(TEST_DOCUMENT_PATH, mode='rb') as file_object:
            self.document.new_version(file_object=file_object)

    def _request_document_version_revert(self):
        return self.delete(
            viewname='rest_api:documentversion-detail', args=(
                self.document.pk, self.document.latest_version.pk
            )
        )

    def test_document_version_revert_no_permission(self):
        self.document = self.upload_document()
        self._create_new_version()
        response = self._request_document_version_revert()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_document_version_revert_with_access(self):
        self.document = self.upload_document()
        self._create_new_version()
        self.grant_access(
            permission=permission_document_version_revert, obj=self.document
        )
        response = self._request_document_version_revert()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(self.document.versions.count(), 1)
        self.assertEqual(
            self.document.versions.first(), self.document.latest_version
        )

    def _request_document_version_list(self):
        return self.get(
            viewname='rest_api:document-version-list', args=(self.document.pk,)
        )

    def test_document_version_list_no_permission(self):
        self.document = self.upload_document()
        self._create_new_version()
        response = self._request_document_version_list()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

    def test_document_version_list_with_access(self):
        self.document = self.upload_document()
        self._create_new_version()
        self.grant_access(
            permission=permission_document_version_view, obj=self.document
        )
        response = self._request_document_version_list()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['results'][1]['checksum'],
            self.document.latest_version.checksum
        )

    def _request_document_download(self):
        return self.get(
            viewname='rest_api:document-download', args=(self.document.pk,)
        )

    def test_document_download_no_permission(self):
        self.document = self.upload_document()
        response = self._request_document_download()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_document_download_with_access(self):
        self.document = self.upload_document()
        self.grant_access(
            permission=permission_document_download, obj=self.document
        )
        response = self._request_document_download()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        with self.document.open() as file_object:
            assert_download_response(
                self, response, content=file_object.read(),
                basename=TEST_SMALL_DOCUMENT_FILENAME,
                mime_type='{}; charset=utf-8'.format(
                    self.document.file_mimetype
                )
            )

    def _request_document_version_download(self):
        return self.get(
            viewname='rest_api:documentversion-download', args=(
                self.document.pk, self.document.latest_version.pk,
            )
        )

    def test_document_version_download_no_permission(self):
        self.document = self.upload_document()
        response = self._request_document_version_download()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_document_version_download_with_access(self):
        self.document = self.upload_document()
        self.grant_access(
            permission=permission_document_download, obj=self.document
        )
        response = self._request_document_version_download()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        with self.document.latest_version.open() as file_object:
            assert_download_response(
                self, response, content=file_object.read(),
                basename=force_text(self.document.latest_version),
                mime_type='{}; charset=utf-8'.format(
                    self.document.file_mimetype
                )
            )

    def test_document_version_download_preserve_extension(self):
        self.login_admin_user()
        self.document = self.upload_document()

        response = self.get(
            viewname='rest_api:documentversion-download', args=(
                self.document.pk, self.document.latest_version.pk,
            ), data={'preserve_extension': True}
        )

        with self.document.latest_version.open() as file_object:
            assert_download_response(
                self, response, content=file_object.read(),
                basename=self.document.latest_version.get_rendered_string(
                    preserve_extension=True
                ), mime_type='{}; charset=utf-8'.format(
                    self.document.file_mimetype
                )
            )

    def _request_document_version_edit_via_patch(self):
        return self.patch(
            viewname='rest_api:documentversion-detail', args=(
                self.document.pk, self.document.latest_version.pk,
            ), data={'comment': TEST_DOCUMENT_VERSION_COMMENT_EDITED}
        )

    def test_document_version_edit_via_patch_no_permission(self):
        self.document = self.upload_document()
        response = self._request_document_version_edit_via_patch()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_document_version_edit_via_patch_with_access(self):
        self.document = self.upload_document()
        self.grant_access(
            permission=permission_document_edit, obj=self.document
        )
        response = self._request_document_version_edit_via_patch()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.document.latest_version.refresh_from_db()
        self.assertEqual(self.document.versions.count(), 1)
        self.assertEqual(
            self.document.latest_version.comment,
            TEST_DOCUMENT_VERSION_COMMENT_EDITED
        )

    def _request_document_version_edit_via_put(self):
        return self.put(
            viewname='rest_api:documentversion-detail', args=(
                self.document.pk, self.document.latest_version.pk,
            ), data={'comment': TEST_DOCUMENT_VERSION_COMMENT_EDITED}
        )

    def test_document_version_edit_via_put_no_permission(self):
        self.document = self.upload_document()
        response = self._request_document_version_edit_via_put()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_document_version_edit_via_put_with_access(self):
        self.document = self.upload_document()
        self.grant_access(
            permission=permission_document_edit, obj=self.document
        )
        response = self._request_document_version_edit_via_put()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.document.latest_version.refresh_from_db()
        self.assertEqual(self.document.versions.count(), 1)
        self.assertEqual(
            self.document.latest_version.comment,
            TEST_DOCUMENT_VERSION_COMMENT_EDITED
        )

    def _request_document_description_edit_via_patch(self):
        return self.patch(
            viewname='rest_api:document-detail', args=(self.document.pk,),
            data={'description': TEST_DOCUMENT_DESCRIPTION_EDITED}
        )

    def test_document_description_edit_via_patch_no_permission(self):
        self.document = self.upload_document()
        response = self._request_document_description_edit_via_patch()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_document_description_edit_via_patch_with_access(self):
        self.document = self.upload_document()
        self.grant_access(
            permission=permission_document_properties_edit, obj=self.document
        )
        response = self._request_document_description_edit_via_patch()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.document.refresh_from_db()
        self.assertEqual(
            self.document.description,
            TEST_DOCUMENT_DESCRIPTION_EDITED
        )

    def _request_document_description_edit_via_put(self):
        return self.put(
            viewname='rest_api:document-detail', args=(self.document.pk,),
            data={'description': TEST_DOCUMENT_DESCRIPTION_EDITED}
        )

    def test_document_description_edit_via_put_no_permission(self):
        self.document = self.upload_document()
        response = self._request_document_description_edit_via_put()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_document_description_edit_via_put_with_access(self):
        self.document = self.upload_document()
        self.grant_access(
            permission=permission_document_properties_edit, obj=self.document
        )
        response = self._request_document_description_edit_via_put()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.document.refresh_from_db()
        self.assertEqual(
            self.document.description,
            TEST_DOCUMENT_DESCRIPTION_EDITED
        )


@override_settings(OCR_AUTO_OCR=False)
class DocumentPageAPITestCase(DocumentTestMixin, BaseAPITestCase):
    def setUp(self):
        super(DocumentPageAPITestCase, self).setUp()
        self.login_user()

    def _request_document_page_image(self):
        page = self.document.pages.first()
        return self.get(
            viewname='rest_api:documentpage-image', args=(
                page.document.pk, page.document_version.pk, page.pk
            ),
        )

    def test_document_page_image_view_no_access(self):
        response = self._request_document_page_image()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_document_page_image_view_with_access(self):
        self.grant_access(
            permission=permission_document_view, obj=self.document
        )
        response = self._request_document_page_image()
        self.assertEqual(response.status_code, status.HTTP_200_OK)


@override_settings(OCR_AUTO_OCR=False)
class TrashedDocumentAPITestCase(DocumentTestMixin, BaseAPITestCase):
    auto_upload_document = False

    def setUp(self):
        super(TrashedDocumentAPITestCase, self).setUp()
        self.login_user()

    def _request_document_move_to_trash(self):
        return self.delete(
            viewname='rest_api:document-detail', args=(self.document.pk,)
        )

    def test_document_move_to_trash_no_permission(self):
        self.document = self.upload_document()
        response = self._request_document_move_to_trash()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_document_move_to_trash_with_access(self):
        self.expected_content_type = None

        self.document = self.upload_document()
        self.grant_access(
            permission=permission_document_trash, obj=self.document
        )
        response = self._request_document_move_to_trash()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(Document.objects.count(), 0)
        self.assertEqual(Document.trash.count(), 1)

    def _request_trashed_document_delete_view(self):
        return self.delete(
            viewname='rest_api:trasheddocument-detail', args=(self.document.pk,)
        )

    def test_trashed_document_delete_from_trash_no_access(self):
        self.document = self.upload_document()
        self.document.delete()
        response = self._request_trashed_document_delete_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Document.objects.count(), 0)
        self.assertEqual(Document.trash.count(), 1)

    def test_trashed_document_delete_from_trash_with_access(self):
        self.expected_content_type = None

        self.document = self.upload_document()
        self.document.delete()
        self.grant_access(permission=permission_document_delete, obj=self.document)
        response = self._request_trashed_document_delete_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Document.objects.count(), 0)
        self.assertEqual(Document.trash.count(), 0)

    def _request_trashed_document_detail_view(self):
        return self.get(
            viewname='rest_api:trasheddocument-detail', args=(self.document.pk,)
        )

    def test_trashed_document_detail_view_no_access(self):
        self.document = self.upload_document()
        self.document.delete()
        response = self._request_trashed_document_detail_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse('uuid' in response.data)

    def test_trashed_document_detail_view_with_access(self):
        self.document = self.upload_document()
        self.document.delete()
        self.grant_access(permission=permission_document_view, obj=self.document)
        response = self._request_trashed_document_detail_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['uuid'], force_text(self.document.uuid))

    def _request_trashed_document_list_view(self):
        return self.get(
            viewname='rest_api:trasheddocument-list'
        )

    def test_trashed_document_list_view_no_access(self):
        self.document = self.upload_document()
        self.document.delete()
        response = self._request_trashed_document_list_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

    def test_trashed_document_list_view_with_access(self):
        self.document = self.upload_document()
        self.document.delete()
        self.grant_access(
            permission=permission_document_view, obj=self.document
        )
        response = self._request_trashed_document_list_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['results'][0]['uuid'], force_text(self.document.uuid)
        )

    def _request_trashed_document_restore_view(self):
        return self.post(
            viewname='rest_api:trasheddocument-restore', args=(self.document.pk,)
        )

    def test_trashed_document_restore_no_access(self):
        self.document = self.upload_document()
        self.document.delete()
        response = self._request_trashed_document_restore_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Document.trash.count(), 1)
        self.assertEqual(Document.objects.count(), 0)

    def test_trashed_document_restore_with_access(self):
        self.document = self.upload_document()
        self.document.delete()
        self.grant_access(permission=permission_document_restore, obj=self.document)
        response = self._request_trashed_document_restore_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Document.trash.count(), 0)
        self.assertEqual(Document.objects.count(), 1)
