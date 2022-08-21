from mayan.apps.common.tests.mixins import ObjectCopyTestMixin
from mayan.apps.documents.tests.mixins.document_mixins import DocumentTestMixin
from mayan.apps.testing.tests.base import BaseTestCase

from .mixins import CabinetTestMixin


class CabinetCopyTestCase(
    CabinetTestMixin, DocumentTestMixin, ObjectCopyTestMixin, BaseTestCase
):
    _test_copy_method = 'get_family'
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_document_stub()
        self._create_test_cabinet()
        self._create_test_cabinet_child()
        self._test_cabinet.document_add(document=self._test_document)
        self._test_object = self._test_cabinet
