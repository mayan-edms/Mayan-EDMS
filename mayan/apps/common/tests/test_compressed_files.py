from __future__ import unicode_literals

from common.tests import BaseTestCase

from ..compressed_files import Archive, TarArchive, ZipArchive

from .literals import (
    TEST_COMPRESSED_FILE_CONTENTS, TEST_FILE_CONTENTS_1, TEST_FILE3_PATH,
    TEST_FILENAME1, TEST_FILENAME3, TEST_TAR_BZ2_FILE_PATH,
    TEST_TAR_FILE_PATH, TEST_TAR_GZ_FILE_PATH, TEST_ZIP_FILE_PATH
)


class TarArchiveClassTestCase(BaseTestCase):
    archive_path = TEST_TAR_FILE_PATH
    cls = TarArchive
    filename = TEST_FILENAME3
    file_path = TEST_FILE3_PATH
    members_list = TEST_COMPRESSED_FILE_CONTENTS
    member_name = TEST_FILENAME1
    member_contents = TEST_FILE_CONTENTS_1

    def test_add_file(self):
        archive = self.cls()
        archive.create()
        with open(self.file_path, mode='rb') as file_object:
            archive.add_file(file_object=file_object, filename=self.filename)
            self.assertTrue(archive.members(), [self.filename])

    def test_open(self):
        with open(self.archive_path, mode='rb') as file_object:
            archive = Archive.open(file_object=file_object)
            self.assertTrue(isinstance(archive, self.cls))

    def test_members(self):
        with open(self.archive_path, mode='rb') as file_object:
            archive = Archive.open(file_object=file_object)
            self.assertEqual(archive.members(), self.members_list)

    def test_member_contents(self):
        with open(self.archive_path, mode='rb') as file_object:
            archive = Archive.open(file_object=file_object)
            self.assertEqual(
                archive.member_contents(filename=self.member_name),
                self.member_contents
            )

    def test_open_member(self):
        with open(self.archive_path, mode='rb') as file_object:
            archive = Archive.open(file_object=file_object)
            file_object = archive.open_member(filename=self.member_name)
            self.assertEqual(
                file_object.read(), self.member_contents
            )


class ZipArchiveClassTestCase(TarArchiveClassTestCase):
    archive_path = TEST_ZIP_FILE_PATH
    cls = ZipArchive


class TarGzArchiveClassTestCase(TarArchiveClassTestCase):
    archive_path = TEST_TAR_GZ_FILE_PATH
    cls = TarArchive


class TarBz2ArchiveClassTestCase(TarArchiveClassTestCase):
    archive_path = TEST_TAR_BZ2_FILE_PATH
    cls = TarArchive
