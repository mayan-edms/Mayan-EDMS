from pathlib import Path

import shutil

from mayan.apps.storage.utils import mkdtemp
from mayan.apps.testing.tests.base import BaseTestCase
from mayan.apps.testing.tests.utils import mute_stdout

from .mocks import TestDependency


class DependencyClassTestCase(BaseTestCase):
    def setUp(self):
        super(DependencyClassTestCase, self).setUp()

        self.test_replace_text = 'replaced_text'

        self.temporary_directory = mkdtemp()
        self.path_temporary_directory = Path(self.temporary_directory)
        self.path_test_file = self.path_temporary_directory / 'test_file.css'

        with self.path_test_file.open(mode='w') as file_object:
            file_object.write(
                '@import url("https://fonts.googleapis.com/css?family=Lato:400,700,400italic");'
            )
        self.test_dependency = TestDependency(
            name='test_dependency', module=__name__
        )

    def tearDown(self):
        super(DependencyClassTestCase, self).tearDown()
        shutil.rmtree(path=self.temporary_directory, ignore_errors=True)

    def _patch_test_file(self):
        replace_list = [
            {
                'filename_pattern': '*',
                'content_patterns': [
                    {
                        'search': '"https://fonts.googleapis.com/css?family=Lato:400,700,400italic"',
                        'replace': self.test_replace_text,
                    }
                ]
            }
        ]

        with mute_stdout():
            self.test_dependency.patch_files(
                path=self.temporary_directory, replace_list=replace_list
            )

        with self.path_test_file.open(mode='r') as file_object:
            self.final_text = file_object.read()

    def test_file_patching(self):
        self._patch_test_file()

        self.assertEqual(
            self.final_text, '@import url({});'.format(self.test_replace_text)
        )
