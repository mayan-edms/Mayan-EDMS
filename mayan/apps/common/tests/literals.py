from __future__ import unicode_literals

import os

from django.conf import settings

EXCLUDE_TEST_TAG = 'exclude'

TEST_ERROR_LOG_ENTRY_RESULT = 'test_error_log_entry_result_text'
TEST_VIEW_NAME = 'test view name'
TEST_VIEW_URL = 'test-view-url'

# Filenames
TEST_ARCHIVE_ZIP_SPECIAL_CHARACTERS_FILENAME_MEMBER = 'test_archvive_with_special_characters_filename_member.zip'
TEST_ARCHIVE_ZIP_CP437_MEMBER = 'test_archvive_with_cp437_member.zip'
TEST_FILENAME1 = 'test_file1.txt'
TEST_FILENAME2 = 'test_file2.txt'
TEST_FILENAME3 = 'test_file3.txt'
TEST_FILE_CONTENTS_1 = b'TEST FILE 1\n'
TEST_FILE_CONTENTS_2 = 'TEST FILE 2\n'
TEST_TAR_BZ2_FILE = 'test_file.tar.bz2'
TEST_TAR_FILE = 'test_file.tar'
TEST_TAR_GZ_FILE = 'test_file.tar.gz'
TEST_ZIP_FILE = 'test_file.zip'
TEST_COMPRESSED_FILE_CONTENTS = [TEST_FILENAME1, TEST_FILENAME2]

# File paths
TEST_ARCHIVE_ZIP_SPECIAL_CHARACTERS_FILENAME_MEMBER_PATH = os.path.join(
    settings.BASE_DIR, 'apps', 'common', 'tests', 'contrib',
    TEST_ARCHIVE_ZIP_SPECIAL_CHARACTERS_FILENAME_MEMBER
)
TEST_ARCHIVE_ZIP_CP437_MEMBER_PATH = os.path.join(
    settings.BASE_DIR, 'apps', 'common', 'tests', 'contrib',
    TEST_ARCHIVE_ZIP_CP437_MEMBER
)
TEST_FILE3_PATH = os.path.join(
    settings.BASE_DIR, 'apps', 'common', 'tests', 'contrib', TEST_FILENAME3
)
TEST_TAR_BZ2_FILE_PATH = os.path.join(
    settings.BASE_DIR, 'apps', 'common', 'tests', 'contrib', TEST_TAR_BZ2_FILE
)
TEST_TAR_FILE_PATH = os.path.join(
    settings.BASE_DIR, 'apps', 'common', 'tests', 'contrib', TEST_TAR_FILE
)
TEST_TAR_GZ_FILE_PATH = os.path.join(
    settings.BASE_DIR, 'apps', 'common', 'tests', 'contrib', TEST_TAR_GZ_FILE
)
TEST_ZIP_FILE_PATH = os.path.join(
    settings.BASE_DIR, 'apps', 'common', 'tests', 'contrib', TEST_ZIP_FILE
)

TEST_SERVER_HOST = 'testserver'
TEST_SERVER_SCHEME = 'http'
