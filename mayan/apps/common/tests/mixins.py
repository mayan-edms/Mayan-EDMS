from __future__ import unicode_literals

import os

import psutil

from ..settings import setting_temporary_directory


class TempfileCheckMixin(object):
    def _get_temporary_entries_count(self):
        return len(os.listdir(setting_temporary_directory.value))

    def setUp(self):
        super(TempfileCheckMixin, self).setUp()
        self._temporary_items = self._get_temporary_entries_count()

    def tearDown(self):
        self.assertEqual(
            self._temporary_items, self._get_temporary_entries_count(),
            msg='Orphan temporary file. The number of temporary file and '
            'directories at the start and at the end of the test are not the '
            'same.'
        )
        super(TempfileCheckMixin, self).tearDown()


class FileDescriptorCheckMixin(object):
    def _get_descriptor_count(self):
        process = psutil.Process()
        return process.num_fds()

    def setUp(self):
        super(FileDescriptorCheckMixin, self).setUp()
        self._descriptor_count = self._get_descriptor_count()

    def tearDown(self):
        self.assertEqual(
            self._descriptor_count, self._get_descriptor_count(),
            msg='File descriptor leak. The number of file descriptors at '
            'the start and at the end of the test are not the same.'
        )
        super(FileDescriptorCheckMixin, self).tearDown()

