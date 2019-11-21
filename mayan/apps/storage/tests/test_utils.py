from __future__ import print_function, unicode_literals

from pathlib2 import Path
import shutil

from mayan.apps.common.tests.base import BaseTestCase
from mayan.apps.storage.utils import mkdtemp

from ..utils import patch_files


class PatchFilesTestCase(BaseTestCase):
    test_replace_text = 'replaced_text'

    def setUp(self):
        super(PatchFilesTestCase, self).setUp()

        self.temporary_directory = mkdtemp()
        self.path_temporary_directory = Path(self.temporary_directory)
        self.path_test_file = self.path_temporary_directory / 'test_file.txt'

        with self.path_test_file.open(mode='w') as file_object:
            file_object.writelines(
                [
                    'line 1\n',
                    '    line 2\n',
                    'line 3\n',
                ]
            )

    def tearDown(self):
        super(PatchFilesTestCase, self).tearDown()
        shutil.rmtree(self.temporary_directory, ignore_errors=True)

    def _patch_test_file(self):
        replace_list = [
            {
                'filename_pattern': '*',
                'content_patterns': [
                    {
                        'search': self.test_search_text,
                        'replace': self.test_replace_text,
                    }
                ]
            }
        ]
        patch_files(
            path=self.path_temporary_directory, replace_list=replace_list
        )

        with self.path_test_file.open(mode='r') as file_object:
            self.final_text = file_object.read()

    def test_file_patching_single_line(self):
        self.test_search_text = 'line 1'

        self._patch_test_file()

        self.assertEqual(self.final_text, 'replaced_text\n    line 2\nline 3\n')

    def test_file_patching_multi_line(self):
        self.test_search_text = 'line 2\nline 3\n'

        self._patch_test_file()

        self.assertEqual(self.final_text, 'line 1\n    replaced_text')

    def test_file_patching_spaces(self):
        self.test_search_text = '    line 2'

        self._patch_test_file()

        self.assertEqual(self.final_text, 'line 1\nreplaced_text\nline 3\n')

    def test_file_patching_no_matches(self):
        self.test_search_text = 'line 4'

        self._patch_test_file()

        self.assertEqual(self.final_text, 'line 1\n    line 2\nline 3\n')
