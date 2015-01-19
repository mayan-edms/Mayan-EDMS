from __future__ import unicode_literals

import os

from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.base import File
from django.test import TestCase

from documents.models import Document, DocumentType

from .models import Folder

TEST_DOCUMENT_PATH = os.path.join(settings.BASE_DIR, 'contrib', 'sample_documents', 'title_page.png')


class FolderTestCase(TestCase):
    def setUp(self):
        self.document_type = DocumentType(name='test doc type')
        self.document_type.save()

        self.document = Document(
            document_type=self.document_type,
            description='description',
        )
        self.document.save()

        with open(TEST_DOCUMENT_PATH) as file_object:
            self.document.new_version(file_object=File(file_object))

    def test_creation_of_folder(self):
        user = User.objects.all()[0]
        folder = Folder.objects.create(title='test', user=user)

        self.assertEqual(Folder.objects.all().count(), 1)
        self.assertEqual(list(Folder.objects.all()), [folder])
        folder.delete()

    def test_addition_of_documents(self):
        user = User.objects.all()[0]
        folder = Folder.objects.create(title='test', user=user)
        folder.documents.add(self.document)

        self.assertEqual(folder.documents.count(), 1)
        self.assertEqual(list(folder.documents.all()), [self.document])
        folder.delete()

    def test_addition_and_deletion_of_documents(self):
        user = User.objects.all()[0]
        folder = Folder.objects.create(title='test', user=user)
        folder.documents.add(self.document)

        self.assertEqual(folder.documents.count(), 1)
        self.assertEqual(list(folder.documents.all()), [self.document])

        folder.documents.remove(self.document)

        self.assertEqual(folder.documents.count(), 0)
        self.assertEqual(list(folder.documents.all()), [])

        folder.delete()

    def tearDown(self):
        self.document.delete()
        self.document_type.delete()
