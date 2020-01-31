from __future__ import unicode_literals

import shutil

from mayan.apps.documents.tests.literals import TEST_SMALL_DOCUMENT_PATH
from mayan.apps.storage.utils import fs_cleanup, mkdtemp

from ..literals import SOURCE_CHOICE_WEB_FORM, SOURCE_UNCOMPRESS_CHOICE_Y
from ..models.staging_folder_sources import StagingFolderSource
from ..models.watch_folder_sources import WatchFolderSource
from ..models.webform_sources import WebFormSource

from .literals import (
    TEST_SOURCE_LABEL, TEST_SOURCE_UNCOMPRESS_N, TEST_STAGING_PREVIEW_WIDTH
)


class StagingFolderTestMixin(object):
    def setUp(self):
        super(StagingFolderTestMixin, self).setUp()
        self.test_staging_folders = []

    def _create_test_stating_folder(self):
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

    def tearDown(self):
        for test_staging_folder in self.test_staging_folders:
            fs_cleanup(filename=test_staging_folder.folder_path)

        super(StagingFolderTestMixin, self).tearDown()


class StagingFolderViewTestMixin(object):
    def _request_staging_file_delete_view(self, staging_folder, staging_file):
        return self.post(
            viewname='sources:staging_file_delete', kwargs={
                'pk': staging_folder.pk,
                'encoded_filename': staging_file.encoded_filename
            }
        )


class SourceTestMixin(object):
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


class SourceViewTestMixin(object):
    def _request_setup_source_list_view(self):
        return self.get(viewname='sources:setup_source_list')

    def _request_setup_source_create_view(self):
        return self.post(
            kwargs={'source_type': SOURCE_CHOICE_WEB_FORM},
            viewname='sources:setup_source_create', data={
                'enabled': True, 'label': TEST_SOURCE_LABEL,
                'uncompress': TEST_SOURCE_UNCOMPRESS_N
            }
        )

    def _request_setup_source_delete_view(self):
        return self.post(
            viewname='sources:setup_source_delete',
            kwargs={'pk': self.test_source.pk}
        )


class WatchFolderTestMixin(object):
    def _create_test_watchfolder(self):
        self.test_watch_folder = WatchFolderSource.objects.create(
            document_type=self.test_document_type,
            folder_path=self.temporary_directory,
            include_subdirectories=False,
            uncompress=SOURCE_UNCOMPRESS_CHOICE_Y
        )
