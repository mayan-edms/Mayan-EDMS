import shutil

from mayan.apps.documents.tests.literals import (
    TEST_DOCUMENT_DESCRIPTION, TEST_SMALL_DOCUMENT_PATH
)
from mayan.apps.storage.utils import fs_cleanup, mkdtemp

from ..literals import SOURCE_CHOICE_WEB_FORM, SOURCE_UNCOMPRESS_CHOICE_Y
from ..models.staging_folder_sources import StagingFolderSource
from ..models.watch_folder_sources import WatchFolderSource
from ..models.webform_sources import WebFormSource

from .literals import (
    TEST_SOURCE_LABEL, TEST_SOURCE_LABEL_EDITED, TEST_SOURCE_UNCOMPRESS_N,
    TEST_STAGING_PREVIEW_WIDTH
)


class DocumentUploadIssueTestMixin:
    def _request_test_source_create_view(self):
        return self.post(
            viewname='sources:setup_source_create', kwargs={
                'source_type_name': SOURCE_CHOICE_WEB_FORM
            }, data={
                'enabled': True, 'label': 'test', 'uncompress': 'n'
            }
        )

    def _request_test_source_edit_view(self):
        return self.post(
            viewname='documents:document_edit', kwargs={
                'document_id': self.test_document.pk
            },
            data={
                'description': TEST_DOCUMENT_DESCRIPTION,
                'label': self.test_document.label,
                'language': self.test_document.language
            }
        )


class DocumentUploadWizardViewTestMixin:
    def _request_upload_wizard_view(self, document_path=TEST_SMALL_DOCUMENT_PATH):
        with open(file=document_path, mode='rb') as file_object:
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


class DocumentVersionUploadViewTestMixin:
    def _request_document_version_upload_view(self, source_file):
        return self.post(
            viewname='sources:document_version_upload', kwargs={
                'document_id': self.test_document.pk,
                'source_id': self.test_source.pk,
            }, data={'source-file': source_file}
        )

    def _request_document_version_upload_no_source_view(self, source_file):
        return self.post(
            viewname='sources:document_version_upload', kwargs={
                'document_id': self.test_document.pk,
            }, data={'source-file': source_file}
        )


class StagingFolderAPIViewTestMixin:
    def setUp(self):
        super(StagingFolderTestMixin, self).setUp()
        self.test_staging_folders = []

    def tearDown(self):
        for test_staging_folder in self.test_staging_folders:
            fs_cleanup(filename=test_staging_folder.folder_path)
            self.test_staging_folders.remove(test_staging_folder)

        super(StagingFolderAPIViewTestMixin, self).tearDown()

    def _request_test_staging_folder_create_api_view(self):
        return self.post(
            viewname='rest_api:stagingfolder-list', data={
                'label': TEST_SOURCE_LABEL,
                'folder_path': mkdtemp(),
                'preview_width': TEST_STAGING_PREVIEW_WIDTH,
                'uncompress': TEST_SOURCE_UNCOMPRESS_N,
            }
        )

        self.test_staging_folder = StagingFolderSource.objects.first()
        self.test_staging_folders.append(self.test_staging_folder)

    def _request_test_staging_folder_delete_api_view(self):
        return self.delete(
            viewname='rest_api:stagingfolder-detail', kwargs={
                'pk': self.test_staging_folder.pk
            }
        )

    def _request_test_staging_folder_edit_api_view(self, extra_data=None, verb='patch'):
        data = {
            'label': TEST_SOURCE_LABEL_EDITED,
        }

        if extra_data:
            data.update(extra_data)

        return getattr(self, verb)(
            viewname='rest_api:stagingfolder-detail', kwargs={
                'pk': self.test_staging_folder.pk
            }, data=data
        )

    def _request_test_staging_folder_list_api_view(self):
        return self.get(viewname='rest_api:stagingfolder-list')


class StagingFolderFileAPIViewTestMixin:
    def _request_test_staging_folder_file_delete_api_view(self):
        return self.delete(
            viewname='rest_api:stagingfolderfile-detail', kwargs={
                'staging_folder_pk': self.test_staging_folder.pk,
                'encoded_filename': self.test_staging_folder_file.encoded_filename
            }
        )

    def _request_test_staging_folder_file_detail_api_view(self):
        return self.get(
            viewname='rest_api:stagingfolderfile-detail', kwargs={
                'staging_folder_pk': self.test_staging_folder.pk,
                'encoded_filename': self.test_staging_folder_file.encoded_filename
            }
        )

    def _request_test_staging_folder_file_upload_api_view(self):
        return self.post(
            viewname='rest_api:stagingfolderfile-upload', kwargs={
                'staging_folder_pk': self.test_staging_folder.pk,
                'encoded_filename': self.test_staging_folder_file.encoded_filename
            }, data={'document_type': self.test_document_type.pk}
        )


class StagingFolderTestMixin:
    def setUp(self):
        super(StagingFolderTestMixin, self).setUp()
        self.test_staging_folders = []

    def tearDown(self):
        for test_staging_folder in self.test_staging_folders:
            fs_cleanup(filename=test_staging_folder.folder_path)
            self.test_staging_folders.remove(test_staging_folder)

        super(StagingFolderTestMixin, self).tearDown()

    def _create_test_staging_folder(self):
        self.test_staging_folder = StagingFolderSource.objects.create(
            label=TEST_SOURCE_LABEL,
            folder_path=mkdtemp(),
            preview_width=TEST_STAGING_PREVIEW_WIDTH,
            uncompress=TEST_SOURCE_UNCOMPRESS_N,
        )
        self.test_staging_folders.append(self.test_staging_folder)

    def _copy_test_document(self):
        shutil.copy(
            src=TEST_SMALL_DOCUMENT_PATH,
            dst=self.test_staging_folder.folder_path
        )
        self.test_staging_folder_file = list(
            self.test_staging_folder.get_files()
        )[0]


class StagingFolderViewTestMixin:
    def _request_test_staging_file_delete_view(self, staging_folder, staging_file):
        return self.post(
            viewname='sources:staging_file_delete', kwargs={
                'staging_folder_id': staging_folder.pk,
                'encoded_filename': staging_file.encoded_filename
            }
        )


class SourceTestMixin:
    auto_create_test_source = True

    def setUp(self):
        super(SourceTestMixin, self).setUp()
        if self.auto_create_test_source:
            self._create_test_source()

    def _create_test_source(self):
        self.test_source = WebFormSource.objects.create(
            enabled=True, label=TEST_SOURCE_LABEL,
            uncompress=TEST_SOURCE_UNCOMPRESS_N
        )


class SourceViewTestMixin:
    def _request_setup_source_list_view(self):
        return self.get(viewname='sources:setup_source_list')

    def _request_setup_source_check_get_view(self):
        return self.get(
            viewname='sources:setup_source_check', kwargs={
                'source_id': self.test_source.pk
            }
        )

    def _request_setup_source_create_view(self):
        return self.post(
            kwargs={
                'source_type_name': SOURCE_CHOICE_WEB_FORM
            }, viewname='sources:setup_source_create', data={
                'enabled': True, 'label': TEST_SOURCE_LABEL,
                'uncompress': TEST_SOURCE_UNCOMPRESS_N
            }
        )

    def _request_setup_source_delete_view(self):
        return self.post(
            viewname='sources:setup_source_delete', kwargs={
                'source_id': self.test_source.pk
            }
        )

    def _request_setup_source_edit_view(self):
        return self.post(
            viewname='sources:setup_source_edit', kwargs={
                'source_id': self.test_source.pk
            }, data={
                'label': TEST_SOURCE_LABEL_EDITED,
                'uncompress': self.test_source.uncompress
            }
        )


class WatchFolderTestMixin:
    def _create_test_watchfolder(self):
        self.test_watch_folder = WatchFolderSource.objects.create(
            document_type=self.test_document_type,
            folder_path=self.temporary_directory,
            include_subdirectories=False,
            uncompress=SOURCE_UNCOMPRESS_CHOICE_Y
        )
