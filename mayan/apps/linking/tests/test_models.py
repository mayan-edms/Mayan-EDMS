from __future__ import unicode_literals

from mayan.apps.documents.tests.base import GenericDocumentTestCase

from .mixins import SmartLinkTestMixin


class SmartLinkTestCase(SmartLinkTestMixin, GenericDocumentTestCase):
    def setUp(self):
        super(SmartLinkTestCase, self).setUp()
        self._create_test_smart_link(add_test_document_type=True)

    def test_smart_link_dynamic_label(self):
        self.assertEqual(
            self.test_smart_link.get_dynamic_label(document=self.test_document),
            self.test_document.label
        )
