from __future__ import print_function, unicode_literals

from pathlib2 import Path
import shutil

from mayan.apps.common.tests.base import BaseTestCase
from mayan.apps.storage.utils import mkdtemp

from ..classes import Dependency, Provider


class TestProvider(Provider):
    """Test provider"""


class TestDependency(Dependency):
    provider_class = TestProvider


class DependencyClassTestCase(BaseTestCase):
    def test_file_patching(self):
        test_replace_text = 'replaced_text'

        temporary_directory = mkdtemp()
        path_temporary_directory = Path(temporary_directory)
        path_test_file = path_temporary_directory / 'test_file.css'

        with path_test_file.open(mode='w') as file_object:
            file_object.write(
                '@import url("https://fonts.googleapis.com/css?family=Lato:400,700,400italic");'
            )

        dependency = TestDependency(name='test_dependency', module=__name__)
        replace_list = [
            {
                'filename_pattern': '*',
                'content_patterns': [
                    {
                        'search': '"https://fonts.googleapis.com/css?family=Lato:400,700,400italic"',
                        'replace': test_replace_text,
                    }
                ]
            }
        ]

        dependency.patch_files(path=temporary_directory, replace_list=replace_list)

        with path_test_file.open(mode='r') as file_object:
            final_text = file_object.read()

        shutil.rmtree(temporary_directory, ignore_errors=True)

        self.assertEqual(final_text, '@import url({});'.format(test_replace_text))
