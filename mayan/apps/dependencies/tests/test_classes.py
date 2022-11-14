from pathlib import Path
import shutil

from mayan.apps.storage.utils import TemporaryDirectory, mkdtemp
from mayan.apps.testing.tests.base import BaseTestCase
from mayan.apps.testing.tests.utils import mute_stdout

from ..classes import JavaScriptDependency
from ..exceptions import DependenciesException

from .mocks import TestDependency
from .literals import TEST_TAR_CVE_2007_4559_FILENAME, TEST_TAR_CVE_2007_4559_PATH


class DependencyClassTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()

        self.test_replace_text = 'replaced_text'

        self.temporary_directory = mkdtemp()
        self.path_temporary_directory = Path(self.temporary_directory)
        self.path_test_file = self.path_temporary_directory / 'test_file.css'

        with self.path_test_file.open(mode='w') as file_object:
            file_object.write(
                '@import url("https://fonts.googleapis.com/css?family=Lato:400,700,400italic");'
            )
        self._test_dependency = TestDependency(
            name='test_dependency', module=__name__
        )

    def tearDown(self):
        super().tearDown()
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
            self._test_dependency.patch_files(
                path=self.temporary_directory, replace_list=replace_list
            )

        with self.path_test_file.open(mode='r') as file_object:
            self.final_text = file_object.read()

    def test_file_patching(self):
        self._patch_test_file()

        self.assertEqual(
            self.final_text, '@import url({});'.format(self.test_replace_text)
        )


class DependencyClassCVE_2007_4559TestCase(BaseTestCase):
    def test_path_travesal_detection(self):
        with TemporaryDirectory() as temporary_directory:
            (Path(temporary_directory) / 'package').mkdir()
            with Path(TEST_TAR_CVE_2007_4559_PATH).open(mode='rb') as test_source_file_object:
                with (Path(temporary_directory) / TEST_TAR_CVE_2007_4559_FILENAME).open(mode='wb') as test_destination_file_object:
                    shutil.copyfileobj(fsrc=test_source_file_object, fdst=test_destination_file_object)

            test_dependency = JavaScriptDependency(
                label='Label', module=__name__,
                name='test_repository', version_string='=1.0'
            )
            test_dependency.path_cache = temporary_directory
            test_dependency.version_metadata = {
                'dist': {'tarball': TEST_TAR_CVE_2007_4559_FILENAME}
            }

            with self.assertRaises(expected_exception=DependenciesException):
                test_dependency.extract()
