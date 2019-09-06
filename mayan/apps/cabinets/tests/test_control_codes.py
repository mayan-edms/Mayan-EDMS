from __future__ import unicode_literals

from mayan.apps.documents.tests.base import GenericDocumentTestCase
from mayan.apps.storage.utils import fs_cleanup, mkstemp

from ..control_codes import ControlCodeCabinetDocumentAdd

from .mixins import CabinetTestMixin, CabinetViewTestMixin


class ControlCodeCabinetDocumentAddTestCase(
    CabinetTestMixin, CabinetViewTestMixin,
    GenericDocumentTestCase
):
    auto_upload_document = False

    def setUp(self):
        super(ControlCodeCabinetDocumentAddTestCase, self).setUp()
        self.test_document_path = mkstemp()[1]

        self._create_test_cabinet()
        self._create_test_cabinet_child()

    def tearDown(self):
        fs_cleanup(filename=self.test_document_path)
        super(ControlCodeCabinetDocumentAddTestCase, self).tearDown()

    def test_control_code(self):
        with open(self.test_document_path, mode='wb') as file_object:
            control_code = ControlCodeCabinetDocumentAdd(
                label_path=(
                    self.test_cabinet.label, self.test_cabinet_child.label
                ),
            )
            control_code.get_image().save(file_object)

        self.upload_document()
        self.assertEqual(
            self.test_document.cabinets.first(), self.test_cabinet_child
        )
