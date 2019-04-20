from __future__ import unicode_literals

from mayan.apps.documents.tests import GenericDocumentTestCase

from ..models import SmartLink

from .literals import TEST_SMART_LINK_LABEL, TEST_SMART_LINK_DYNAMIC_LABEL


class SmartLinkTestCase(GenericDocumentTestCase):
    def test_dynamic_label(self):
        smart_link = SmartLink.objects.create(
            label=TEST_SMART_LINK_LABEL,
            dynamic_label=TEST_SMART_LINK_DYNAMIC_LABEL
        )
        smart_link.document_types.add(self.test_document_type)

        self.assertEqual(
            smart_link.get_dynamic_label(document=self.test_document),
            self.test_document.label
        )
