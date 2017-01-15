from __future__ import unicode_literals

import glob
import os

import psutil

from ..settings import setting_temporary_directory


class ContentTypeCheckMixin(object):
    expected_content_type = 'text/html; charset=utf-8'

    def _pre_setup(self):
        super(ContentTypeCheckMixin, self)._pre_setup()
        test_instance = self

        class CustomClient(self.client_class):
            def request(self, *args, **kwargs):
                response = super(CustomClient, self).request(*args, **kwargs)

                content_type = response._headers['content-type'][1]
                test_instance.assertEqual(
                    content_type, test_instance.expected_content_type,
                    msg='Unexpected response content type: {}, expected: {}.'.format(
                        content_type, test_instance.expected_content_type
                    )
                )

                return response

        self.client = CustomClient()


class TempfileCheckMixin(object):
    # Ignore the jvmstat instrumentation and GitLab's CI .config files
    ignore_globs = ('hsperfdata_*', '.config', '.cache')

    def _get_temporary_entries(self):
        ignored_result = []

        # Expand globs by joining the temporary directory and then flattening
        # the list of lists into a single list
        for item in self.ignore_globs:
            ignored_result.extend(
                glob.glob(
                    os.path.join(setting_temporary_directory.value, item)
                )
            )

        # Remove the path and leave only the expanded filename
        ignored_result = map(lambda x: os.path.split(x)[-1], ignored_result)

        return set(
            os.listdir(setting_temporary_directory.value)
        ) - set(ignored_result)

    def setUp(self):
        super(TempfileCheckMixin, self).setUp()
        self._temporary_items = self._get_temporary_entries()

    def tearDown(self):
        final_temporary_items = self._get_temporary_entries()
        self.assertEqual(
            self._temporary_items, final_temporary_items,
            msg='Orphan temporary file. The number of temporary files and/or '
            'directories at the start and at the end of the test are not the '
            'same. Orphan entries: {}'.format(
                ','.join(final_temporary_items - self._temporary_items)
            )
        )
        super(TempfileCheckMixin, self).tearDown()


class OpenFileCheckMixin(object):
    def _get_descriptor_count(self):
        process = psutil.Process()
        return process.num_fds()

    def _get_open_files(self):
        process = psutil.Process()
        return process.open_files()

    def setUp(self):
        super(OpenFileCheckMixin, self).setUp()
        self._open_files = self._get_open_files()

    def tearDown(self):
        if not getattr(self, '_skip_file_descriptor_test', False):
            for new_open_file in self._get_open_files():
                self.assertFalse(
                    new_open_file not in self._open_files,
                    msg='File descriptor leak. The number of file descriptors '
                    'at the start and at the end of the test are not the same.'
                )

            self._skip_file_descriptor_test = False

        super(OpenFileCheckMixin, self).tearDown()
