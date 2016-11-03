from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from documents.models import DocumentType
from documents.search import document_search
from documents.tests import TEST_DOCUMENT_TYPE, TEST_SMALL_DOCUMENT_PATH
from user_management.tests import (
    TEST_ADMIN_PASSWORD, TEST_ADMIN_USERNAME, TEST_ADMIN_EMAIL
)


class Issue46TestCase(TestCase):
    """
    Functional tests to make sure issue 46 is fixed
    """

    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(
            username=TEST_ADMIN_USERNAME, email=TEST_ADMIN_EMAIL,
            password=TEST_ADMIN_PASSWORD
        )
        self.client = Client()
        # Login the admin user
        logged_in = self.client.login(
            username=TEST_ADMIN_USERNAME, password=TEST_ADMIN_PASSWORD
        )
        self.assertTrue(logged_in)
        self.assertTrue(self.admin_user.is_authenticated())

        self.document_count = 4

        self.document_type = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE
        )

        # Upload many instances of the same test document
        for i in range(self.document_count):
            with open(TEST_SMALL_DOCUMENT_PATH) as file_object:
                self.document_type.new_document(
                    file_object=file_object,
                    label='test document',
                )

    def tearDown(self):
        for document_type in DocumentType.objects.all():
            document_type.delete()

    def test_advanced_search_past_first_page(self):
        # Make sure all documents are returned by the search
        model_list, result_set, elapsed_time = document_search.search(
            {'label': 'test document'}, user=self.admin_user
        )
        self.assertEqual(len(result_set), self.document_count)

        with self.settings(COMMON_PAGINATE_BY=2):
            # Funcitonal test for the first page of advanced results
            response = self.client.get(
                reverse(
                    'search:results', args=(document_search.get_full_name(),)
                ), {'label': 'test'}
            )

            self.assertContains(
                response, 'Total (1 - 2 out of 4) (Page 1 of 2)',
                status_code=200
            )

            # Functional test for the second page of advanced results
            response = self.client.get(
                reverse(
                    'search:results', args=(document_search.get_full_name(),)
                ), {'label': 'test', 'page': 2}
            )
            self.assertContains(
                response, 'Total (3 - 4 out of 4) (Page 2 of 2)',
                status_code=200
            )
