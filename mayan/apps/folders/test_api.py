from __future__ import unicode_literals

from json import loads

from django.contrib.auth.models import User
from django.core.files import File
from django.core.urlresolvers import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from documents.test_models import (
    TEST_ADMIN_EMAIL, TEST_ADMIN_PASSWORD, TEST_ADMIN_USERNAME,
    TEST_DOCUMENT_FILENAME, TEST_DOCUMENT_PATH, TEST_DOCUMENT_TYPE,
    TEST_SMALL_DOCUMENT_FILENAME, TEST_SMALL_DOCUMENT_PATH,
)

from .models import Folder


TEST_FOLDER_LABEL = 'test folder'


class FolderAPITestCase(APITestCase):
    """
    Test the folder API endpoints
    """

    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username=TEST_ADMIN_USERNAME, email=TEST_ADMIN_EMAIL,
            password=TEST_ADMIN_PASSWORD
        )

        self.client.force_authenticate(user=self.admin_user)

    def testDown(self):
        self.admin_user.delete()

    def test_folder_create(self):
        self.client.post(reverse('rest_api:folder-list'), {'label': TEST_FOLDER_LABEL})

        folder = Folder.objects.first()

        self.assertEqual(Folder.objects.count(), 1)
        self.assertEqual(folder.label, TEST_FOLDER_LABEL)
        self.assertEqual(folder.user, self.admin_user)
