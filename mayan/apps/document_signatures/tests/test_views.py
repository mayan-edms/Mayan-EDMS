from __future__ import absolute_import, unicode_literals

from django.core.files import File

from django_downloadview.test import assert_download_response

from django_gpg.models import Key
from documents.tests.literals import TEST_DOCUMENT_PATH
from documents.tests.test_views import GenericDocumentViewTestCase
from user_management.tests import (
    TEST_USER_USERNAME, TEST_USER_PASSWORD
)

from ..models import DetachedSignature
from ..permissions import (
    permission_document_version_signature_view,
    permission_document_version_signature_delete,
    permission_document_version_signature_download,
    permission_document_version_signature_upload,
)

from .literals import TEST_SIGNATURE_FILE_PATH, TEST_KEY_FILE


class SignaturesViewTestCase(GenericDocumentViewTestCase):
    def test_signature_list_view_no_permission(self):
        with open(TEST_KEY_FILE) as file_object:
            Key.objects.create(key_data=file_object.read())

        with open(TEST_DOCUMENT_PATH) as file_object:
            document = self.document_type.new_document(
                file_object=file_object
            )

        with open(TEST_SIGNATURE_FILE_PATH) as file_object:
            DetachedSignature.objects.create(
                document_version=document.latest_version,
                signature_file=File(file_object)
            )

        self.login(username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)

        response = self.get(
            'signatures:document_version_signature_list',
            args=(document.latest_version.pk,)
        )

        self.assertContains(response, 'Total: 0', status_code=200)

    def test_signature_list_view_with_permission(self):
        with open(TEST_KEY_FILE) as file_object:
            Key.objects.create(key_data=file_object.read())

        with open(TEST_DOCUMENT_PATH) as file_object:
            document = self.document_type.new_document(
                file_object=file_object
            )

        with open(TEST_SIGNATURE_FILE_PATH) as file_object:
            DetachedSignature.objects.create(
                document_version=document.latest_version,
                signature_file=File(file_object)
            )

        self.login(username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)

        self.role.permissions.add(
            permission_document_version_signature_view.stored_permission
        )

        response = self.get(
            'signatures:document_version_signature_list',
            args=(document.latest_version.pk,)
        )

        self.assertContains(response, 'Total: 1', status_code=200)

    def test_signature_detail_view_no_permission(self):
        with open(TEST_KEY_FILE) as file_object:
            Key.objects.create(key_data=file_object.read())

        with open(TEST_DOCUMENT_PATH) as file_object:
            document = self.document_type.new_document(
                file_object=file_object
            )

        with open(TEST_SIGNATURE_FILE_PATH) as file_object:
            signature = DetachedSignature.objects.create(
                document_version=document.latest_version,
                signature_file=File(file_object)
            )

        self.login(username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)

        response = self.get(
            'signatures:document_version_signature_details',
            args=(signature.pk,)
        )

        self.assertEqual(response.status_code, 403)

    def test_signature_detail_view_with_permission(self):
        with open(TEST_KEY_FILE) as file_object:
            Key.objects.create(key_data=file_object.read())

        with open(TEST_DOCUMENT_PATH) as file_object:
            document = self.document_type.new_document(
                file_object=file_object
            )

        with open(TEST_SIGNATURE_FILE_PATH) as file_object:
            signature = DetachedSignature.objects.create(
                document_version=document.latest_version,
                signature_file=File(file_object)
            )

        self.login(username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)

        self.role.permissions.add(
            permission_document_version_signature_view.stored_permission
        )

        response = self.get(
            'signatures:document_version_signature_details',
            args=(signature.pk,)
        )

        self.assertContains(response, signature.signature_id, status_code=200)

    def test_signature_upload_view_no_permission(self):
        with open(TEST_DOCUMENT_PATH) as file_object:
            document = self.document_type.new_document(
                file_object=file_object
            )

        self.login(username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)

        with open(TEST_SIGNATURE_FILE_PATH) as file_object:
            response = self.post(
                'signatures:document_version_signature_upload',
                args=(document.latest_version.pk,),
                data={'signature_file': file_object}
            )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(DetachedSignature.objects.count(), 0)

    def test_signature_upload_view_with_permission(self):
        with open(TEST_DOCUMENT_PATH) as file_object:
            document = self.document_type.new_document(
                file_object=file_object
            )

        self.login(username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)

        self.role.permissions.add(
            permission_document_version_signature_upload.stored_permission
        )

        with open(TEST_SIGNATURE_FILE_PATH) as file_object:
            response = self.post(
                'signatures:document_version_signature_upload',
                args=(document.latest_version.pk,),
                data={'signature_file': file_object}
            )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(DetachedSignature.objects.count(), 1)

    def test_signature_download_view_no_permission(self):
        with open(TEST_DOCUMENT_PATH) as file_object:
            document = self.document_type.new_document(
                file_object=file_object
            )

        with open(TEST_SIGNATURE_FILE_PATH) as file_object:
            signature = DetachedSignature.objects.create(
                document_version=document.latest_version,
                signature_file=File(file_object)
            )

        self.login(username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)

        response = self.get(
            'signatures:document_version_signature_download',
            args=(signature.pk,),
        )

        self.assertEqual(response.status_code, 403)

    def test_signature_download_view_with_permission(self):
        with open(TEST_DOCUMENT_PATH) as file_object:
            document = self.document_type.new_document(
                file_object=file_object
            )

        with open(TEST_SIGNATURE_FILE_PATH) as file_object:
            signature = DetachedSignature.objects.create(
                document_version=document.latest_version,
                signature_file=File(file_object)
            )

        self.login(username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)

        self.role.permissions.add(
            permission_document_version_signature_download.stored_permission
        )

        response = self.get(
            'signatures:document_version_signature_download',
            args=(signature.pk,),
        )

        assert_download_response(
            self, response=response, content=signature.signature_file.read(),
        )

    def test_signature_delete_view_no_permission(self):
        with open(TEST_KEY_FILE) as file_object:
            Key.objects.create(key_data=file_object.read())

        with open(TEST_DOCUMENT_PATH) as file_object:
            document = self.document_type.new_document(
                file_object=file_object
            )

        with open(TEST_SIGNATURE_FILE_PATH) as file_object:
            signature = DetachedSignature.objects.create(
                document_version=document.latest_version,
                signature_file=File(file_object)
            )

        self.login(username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)

        response = self.post(
            'signatures:document_version_signature_delete',
            args=(signature.pk,)
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(DetachedSignature.objects.count(), 1)

    def test_signature_delete_view_with_permission(self):
        with open(TEST_KEY_FILE) as file_object:
            Key.objects.create(key_data=file_object.read())

        with open(TEST_DOCUMENT_PATH) as file_object:
            document = self.document_type.new_document(
                file_object=file_object
            )

        with open(TEST_SIGNATURE_FILE_PATH) as file_object:
            signature = DetachedSignature.objects.create(
                document_version=document.latest_version,
                signature_file=File(file_object)
            )

        self.login(username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)

        self.role.permissions.add(
            permission_document_version_signature_delete.stored_permission
        )

        response = self.post(
            'signatures:document_version_signature_delete',
            args=(signature.pk,), follow=True
        )

        self.assertContains(response, 'deleted', status_code=200)
        self.assertEqual(DetachedSignature.objects.count(), 0)
