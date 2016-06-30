from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.test import override_settings

from documents.models import DocumentType
from documents.tests import TEST_DOCUMENT_TYPE, TEST_SMALL_DOCUMENT_PATH
from rest_api.tests import GenericAPITestCase


@override_settings(OCR_AUTO_OCR=False)
class SearchAPITestCase(GenericAPITestCase):
    """
    Test the search API endpoints
    """

    def test_search(self):
        document_type = DocumentType.on_organization.create(
            label=TEST_DOCUMENT_TYPE
        )

        with open(TEST_SMALL_DOCUMENT_PATH) as file_object:
            document = document_type.new_document(
                file_object=file_object,
            )

        response = self.client.get(
            '{}?q={}'.format(reverse('rest_api:search-view'), document.label)
        )

        self.assertEqual(response.data['results'][0]['label'], document.label)
        self.assertEqual(response.data['count'], 1)
