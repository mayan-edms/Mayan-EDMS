from io import StringIO
from unittest import mock

from django.core import management

from mayan.apps.cabinets.tests.mixins import CabinetTestMixin
from mayan.apps.document_indexing.tests.mixins import IndexTemplateTestMixin
from mayan.apps.storage.utils import NamedTemporaryFile
from mayan.apps.testing.tests.base import BaseTestCase


class MountCabinetManagementCommandTestCase(CabinetTestMixin, BaseTestCase):
    auto_create_test_cabinet = True

    def _call_command(self, mount_point, label):
        stderr = StringIO()
        stdout = StringIO()
        management.call_command(
            'mirroring_mount_cabinet', label, mount_point, stderr=stderr,
            stdout=stdout
        )
        return stderr.getvalue(), stdout.getvalue()

    @mock.patch('fuse.FUSE', autospec=True)
    def test_cabinet_mount_basic(self, FUSE):
        with NamedTemporaryFile() as file_object:
            FUSE.return_value = None
            self._call_command(
                label=self._test_cabinet.label, mount_point=file_object.name
            )

    @mock.patch('fuse.FUSE', autospec=True)
    def test_cabinet_mount_with_invalid_slug(self, FUSE):
        with NamedTemporaryFile() as file_object:
            FUSE.return_value = None
            with self.assertRaises(expected_exception=SystemExit):
                self._call_command(
                    label='invalid', mount_point=file_object.name
                )


class MountIndexManagementCommandTestCase(
    IndexTemplateTestMixin, BaseTestCase
):
    auto_create_test_index_template = False

    def _call_command(self, mount_point, slug):
        stderr = StringIO()
        stdout = StringIO()
        management.call_command(
            'mirroring_mount_index', slug, mount_point, stderr=stderr,
            stdout=stdout
        )
        return stderr.getvalue(), stdout.getvalue()

    def setUp(self):
        super().setUp()
        self._create_test_index_template()

    @mock.patch('fuse.FUSE', autospec=True)
    def test_index_mount_basic(self, FUSE):
        with NamedTemporaryFile() as file_object:
            FUSE.return_value = None
            self._call_command(
                mount_point=file_object.name,
                slug=self._test_index_template.slug
            )

    @mock.patch('fuse.FUSE', autospec=True)
    def test_index_mount_with_invalid_slug(self, FUSE):
        with NamedTemporaryFile() as file_object:
            FUSE.return_value = None
            with self.assertRaises(expected_exception=SystemExit):
                self._call_command(
                    mount_point=file_object.name, slug='invalid'
                )
