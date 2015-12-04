from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.core.files import File
from django.core.urlresolvers import reverse
from django.test import override_settings

from rest_framework.test import APITestCase

from documents.models import DocumentType
from documents.tests import TEST_DOCUMENT_TYPE, TEST_SMALL_DOCUMENT_PATH
from user_management.tests.literals import (
    TEST_ADMIN_EMAIL, TEST_ADMIN_PASSWORD, TEST_ADMIN_USERNAME
)

from ..models import Tag

from .literals import (
    TEST_TAG_COLOR, TEST_TAG_COLOR_EDITED, TEST_TAG_LABEL,
    TEST_TAG_LABEL_EDITED
)


class TagAPITestCase(APITestCase):
    """
    Test the tag API endpoints
    """

    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username=TEST_ADMIN_USERNAME, email=TEST_ADMIN_EMAIL,
            password=TEST_ADMIN_PASSWORD
        )

        self.client.force_authenticate(user=self.admin_user)

    def tearDown(self):
        self.admin_user.delete()

    def test_tag_create(self):
        self.client.post(
            reverse('rest_api:tag-list'), {
                'label': TEST_TAG_LABEL, 'color': TEST_TAG_COLOR
            }
        )

        tag = Tag.objects.first()

        self.assertEqual(Tag.objects.count(), 1)
        self.assertEqual(tag.label, TEST_TAG_LABEL)
        self.assertEqual(tag.color, TEST_TAG_COLOR)

    def test_tag_delete(self):
        tag = Tag.objects.create(color=TEST_TAG_COLOR, label=TEST_TAG_LABEL)

        self.client.delete(reverse('rest_api:tag-detail', args=(tag.pk,)))

        self.assertEqual(Tag.objects.count(), 0)

    def test_tag_edit(self):
        tag = Tag.objects.create(color=TEST_TAG_COLOR, label=TEST_TAG_LABEL)

        self.client.put(
            reverse('rest_api:tag-detail', args=(tag.pk,)),
            {
                'label': TEST_TAG_LABEL_EDITED,
                'color': TEST_TAG_COLOR_EDITED
            }
        )

        tag = Tag.objects.first()

        self.assertEqual(tag.label, TEST_TAG_LABEL_EDITED)
        self.assertEqual(tag.color, TEST_TAG_COLOR_EDITED)

    @override_settings(OCR_AUTO_OCR=False)
    def test_tag_add_document(self):
        tag = Tag.objects.create(color=TEST_TAG_COLOR, label=TEST_TAG_LABEL)

        document_type = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE
        )

        with open(TEST_SMALL_DOCUMENT_PATH) as file_object:
            document = document_type.new_document(
                file_object=File(file_object),
            )

        self.client.post(
            reverse('rest_api:document-tag-list', args=(document.pk,)),
            {'tag': tag.pk}
        )

        self.assertEqual(tag.documents.count(), 1)

    @override_settings(OCR_AUTO_OCR=False)
    def test_tag_remove_document(self):
        tag = Tag.objects.create(color=TEST_TAG_COLOR, label=TEST_TAG_LABEL)

        document_type = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE
        )

        with open(TEST_SMALL_DOCUMENT_PATH) as file_object:
            document = document_type.new_document(
                file_object=File(file_object),
            )

        tag.documents.add(document)

        self.client.delete(
            reverse('rest_api:document-tag', args=(document.pk, tag.pk)),
        )

        self.assertEqual(tag.documents.count(), 0)
