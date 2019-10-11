from __future__ import unicode_literals

import os
import shutil

from mayan.apps.checkouts.models import NewVersionBlock
from mayan.apps.common.tests.base import GenericViewTestCase
from mayan.apps.documents.models import Document
from mayan.apps.documents.permissions import permission_document_create
from mayan.apps.documents.tests.base import GenericDocumentViewTestCase
from mayan.apps.documents.tests.literals import (
    TEST_COMPRESSED_DOCUMENT_PATH, TEST_DOCUMENT_DESCRIPTION,
    TEST_SMALL_DOCUMENT_CHECKSUM, TEST_SMALL_DOCUMENT_PATH
)
from mayan.apps.storage.utils import fs_cleanup, mkdtemp

from ..links import link_document_version_upload
from ..literals import SOURCE_CHOICE_WEB_FORM, SOURCE_UNCOMPRESS_CHOICE_Y
from ..models import StagingFolderSource, WebFormSource
from ..permissions import (
    permission_sources_setup_create, permission_sources_setup_delete,
    permission_sources_setup_view, permission_staging_file_delete
)

from .literals import (
    TEST_SOURCE_LABEL, TEST_SOURCE_UNCOMPRESS_N, TEST_STAGING_PREVIEW_WIDTH
)
from .mixins import SourceTestMixin, SourceViewTestMixin


class DocumentUploadWizardViewTestMixin(object):
    def _request_upload_wizard_view(self, document_path=TEST_SMALL_DOCUMENT_PATH):
        with open(document_path, mode='rb') as file_object:
            return self.post(
                viewname='sources:document_upload_interactive', kwargs={
                    'source_id': self.test_source.pk
                }, data={
                    'source-file': file_object,
                    'document_type_id': self.test_document_type.pk,
                }
            )

    def _request_upload_interactive_view(self):
        return self.get(
            viewname='sources:document_upload_interactive', data={
                'document_type_id': self.test_document_type.pk,
            }
        )


class DocumentUploadWizardViewTestCase(
    SourceTestMixin, DocumentUploadWizardViewTestMixin,
    GenericDocumentViewTestCase
):
    auto_upload_document = False

    def test_upload_compressed_file(self):
        self.test_source.uncompress = SOURCE_UNCOMPRESS_CHOICE_Y
        self.test_source.save()

        self.grant_access(
            obj=self.test_document_type, permission=permission_document_create
        )

        response = self._request_upload_wizard_view(
            document_path=TEST_COMPRESSED_DOCUMENT_PATH
        )
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Document.objects.count(), 2)
        self.assertTrue(
            'first document.pdf' in Document.objects.values_list(
                'label', flat=True
            )
        )
        self.assertTrue(
            'second document.pdf' in Document.objects.values_list(
                'label', flat=True
            )
        )

    def test_upload_wizard_without_permission(self):
        response = self._request_upload_wizard_view()
        self.assertEqual(response.status_code, 403)

        self.assertEqual(Document.objects.count(), 0)

    def test_upload_wizard_with_permission(self):
        self.grant_permission(permission=permission_document_create)

        response = self._request_upload_wizard_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Document.objects.count(), 1)
        self.assertEqual(
            Document.objects.first().checksum, TEST_SMALL_DOCUMENT_CHECKSUM
        )

    def test_upload_wizard_with_document_type_access(self):
        """
        Test uploading of documents by granting the document create
        permssion for the document type to the user
        """
        # Create an access control entry giving the role the document
        # create permission for the selected document type.
        self.grant_access(
            obj=self.test_document_type, permission=permission_document_create
        )

        with open(TEST_SMALL_DOCUMENT_PATH, mode='rb') as file_object:
            response = self.post(
                viewname='sources:document_upload_interactive', kwargs={
                    'source_id': self.test_source.pk
                }, data={
                    'source-file': file_object,
                    'document_type_id': self.test_document_type.pk,
                }
            )
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Document.objects.count(), 1)

    def test_upload_interactive_view_no_permission(self):
        response = self._request_upload_interactive_view()
        self.assertEqual(response.status_code, 403)

    def test_upload_interactive_view_with_access(self):
        self.grant_access(
            permission=permission_document_create, obj=self.test_document_type
        )
        response = self._request_upload_interactive_view()
        self.assertContains(
            response=response, text=self.test_source.label, status_code=200
        )


class DocumentUploadIssueTestCase(GenericDocumentViewTestCase):
    auto_upload_document = False
    auto_login_superuser = True
    auto_login_user = False
    create_test_case_superuser = True
    create_test_case_user = False

    def test_issue_25(self):
        # Create new webform source
        self.post(
            viewname='sources:setup_source_create',
            kwargs={'source_type': SOURCE_CHOICE_WEB_FORM},
            data={'label': 'test', 'uncompress': 'n', 'enabled': True}
        )
        self.assertEqual(WebFormSource.objects.count(), 1)

        # Upload the test document
        with open(TEST_SMALL_DOCUMENT_PATH, mode='rb') as file_object:
            self.post(
                viewname='sources:document_upload_interactive', data={
                    'document-language': 'eng',
                    'source-file': file_object,
                    'document_type_id': self.test_document_type.pk
                }
            )
        self.assertEqual(Document.objects.count(), 1)

        document = Document.objects.first()
        # Test for issue 25 during creation
        # ** description fields was removed from upload from **
        self.assertEqual(document.description, '')

        # Reset description
        document.description = TEST_DOCUMENT_DESCRIPTION
        document.save()
        self.assertEqual(document.description, TEST_DOCUMENT_DESCRIPTION)

        # Test for issue 25 during editing
        self.post(
            viewname='documents:document_edit', kwargs={'pk': document.pk},
            data={
                'description': TEST_DOCUMENT_DESCRIPTION,
                'language': document.language, 'label': document.label
            }
        )
        # Fetch document again and test description
        document = Document.objects.first()
        self.assertEqual(document.description, TEST_DOCUMENT_DESCRIPTION)


class NewDocumentVersionViewTestCase(GenericDocumentViewTestCase):
    auto_login_superuser = True
    auto_login_user = False
    create_test_case_superuser = True
    create_test_case_user = False

    def test_new_version_block(self):
        """
        Gitlab issue #231
        User shown option to upload new version of a document even though it
        is blocked by checkout - v2.0.0b2

        Expected results:
            - Link to upload version view should not resolve
            - Upload version view should reject request
        """
        NewVersionBlock.objects.block(self.test_document)

        response = self.post(
            viewname='sources:document_version_upload', kwargs={
                'document_pk': self.test_document.pk
            }, follow=True
        )

        self.assertContains(
            response=response, text='blocked from uploading',
            status_code=200
        )

        response = self.get(
            viewname='documents:document_version_list', kwargs={
                'pk': self.test_document.pk
            }, follow=True
        )

        # Needed by the url view resolver
        response.context.current_app = None
        resolved_link = link_document_version_upload.resolve(
            context=response.context
        )

        self.assertEqual(resolved_link, None)


class StagingFolderViewTestMixin(object):
    def _request_staging_file_delete_view(self, staging_folder, staging_file):
        return self.post(
            viewname='sources:staging_file_delete', kwargs={
                'pk': staging_folder.pk,
                'encoded_filename': staging_file.encoded_filename
            }
        )


class StagingFolderViewTestCase(
    StagingFolderViewTestMixin, GenericViewTestCase
):
    def setUp(self):
        super(StagingFolderViewTestCase, self).setUp()
        self.temporary_directory = mkdtemp()
        shutil.copy(src=TEST_SMALL_DOCUMENT_PATH, dst=self.temporary_directory)

        self.filename = os.path.basename(TEST_SMALL_DOCUMENT_PATH)

    def tearDown(self):
        fs_cleanup(filename=self.temporary_directory)
        super(StagingFolderViewTestCase, self).tearDown()

    def test_staging_file_delete_no_permission(self):
        staging_folder = StagingFolderSource.objects.create(
            label=TEST_SOURCE_LABEL,
            folder_path=self.temporary_directory,
            preview_width=TEST_STAGING_PREVIEW_WIDTH,
            uncompress=TEST_SOURCE_UNCOMPRESS_N,
        )

        self.assertEqual(len(list(staging_folder.get_files())), 1)

        staging_file = list(staging_folder.get_files())[0]

        response = self._request_staging_file_delete_view(
            staging_folder=staging_folder, staging_file=staging_file
        )
        self.assertEqual(response.status_code, 404)

        self.assertEqual(len(list(staging_folder.get_files())), 1)

    def test_staging_file_delete_with_permission(self):
        self.grant_permission(permission=permission_staging_file_delete)

        staging_folder = StagingFolderSource.objects.create(
            label=TEST_SOURCE_LABEL,
            folder_path=self.temporary_directory,
            preview_width=TEST_STAGING_PREVIEW_WIDTH,
            uncompress=TEST_SOURCE_UNCOMPRESS_N,
        )

        self.assertEqual(len(list(staging_folder.get_files())), 1)

        staging_file = list(staging_folder.get_files())[0]

        response = self._request_staging_file_delete_view(
            staging_folder=staging_folder, staging_file=staging_file
        )
        self.assertEqual(response.status_code, 302)

        self.assertEqual(len(list(staging_folder.get_files())), 0)


class SourcesViewTestCase(
    SourceTestMixin, SourceViewTestMixin, GenericViewTestCase
):
    auto_create_test_source = False

    def test_source_create_view_no_permission(self):
        response = self._request_setup_source_create_view()
        self.assertEqual(response.status_code, 403)

        self.assertEqual(WebFormSource.objects.count(), 0)

    def test_source_create_view_with_permission(self):
        self.grant_permission(permission=permission_sources_setup_create)

        response = self._request_setup_source_create_view()
        self.assertEqual(response.status_code, 302)

        webform_source = WebFormSource.objects.first()
        self.assertEqual(webform_source.label, TEST_SOURCE_LABEL)
        self.assertEqual(webform_source.uncompress, TEST_SOURCE_UNCOMPRESS_N)

    def test_source_delete_view_with_permission(self):
        self._create_test_source()

        self.grant_permission(permission=permission_sources_setup_delete)

        response = self._request_setup_source_delete_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(WebFormSource.objects.count(), 0)

    def test_source_delete_view_no_permission(self):
        self._create_test_source()

        response = self._request_setup_source_delete_view()
        self.assertEqual(response.status_code, 403)

        self.assertEqual(WebFormSource.objects.count(), 1)

    def test_source_list_view_no_permission(self):
        self._create_test_source()

        response = self._request_setup_source_list_view()
        self.assertEqual(response.status_code, 403)

    def test_source_list_view_with_permission(self):
        self._create_test_source()

        self.grant_permission(permission=permission_sources_setup_view)

        response = self._request_setup_source_list_view()
        self.assertContains(
            response=response, text=self.test_source.label, status_code=200
        )
