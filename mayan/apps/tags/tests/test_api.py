from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.test import override_settings

from documents.models import DocumentType
from documents.tests import TEST_DOCUMENT_TYPE, TEST_SMALL_DOCUMENT_PATH
from rest_api.tests.base import GenericAPITestCase

from ..models import Tag

from .literals import (
    TEST_TAG_COLOR, TEST_TAG_COLOR_EDITED, TEST_TAG_LABEL,
    TEST_TAG_LABEL_EDITED
)


class TagAPITestCase(GenericAPITestCase):
    """
    Test the tag API endpoints
    """

    def test_tag_create(self):
        response = self.client.post(
            reverse('rest_api:tag-list'), {
                'label': TEST_TAG_LABEL, 'color': TEST_TAG_COLOR
            }
        )

        self.assertEqual(response.status_code, 201)

        tag = Tag.on_organization.first()

        self.assertEqual(response.data['id'], tag.pk)
        self.assertEqual(response.data['label'], TEST_TAG_LABEL)
        self.assertEqual(response.data['color'], TEST_TAG_COLOR)

        self.assertEqual(Tag.on_organization.count(), 1)
        self.assertEqual(tag.label, TEST_TAG_LABEL)
        self.assertEqual(tag.color, TEST_TAG_COLOR)

    def test_tag_delete(self):
        tag = Tag.on_organization.create(
            color=TEST_TAG_COLOR, label=TEST_TAG_LABEL
        )

        self.client.delete(reverse('rest_api:tag-detail', args=(tag.pk,)))

        self.assertEqual(Tag.on_organization.count(), 0)

    def test_tag_edit(self):
        tag = Tag.on_organization.create(
            color=TEST_TAG_COLOR, label=TEST_TAG_LABEL
        )

        self.client.put(
            reverse('rest_api:tag-detail', args=(tag.pk,)),
            {
                'label': TEST_TAG_LABEL_EDITED,
                'color': TEST_TAG_COLOR_EDITED
            }
        )

        tag = Tag.on_organization.first()

        self.assertEqual(tag.label, TEST_TAG_LABEL_EDITED)
        self.assertEqual(tag.color, TEST_TAG_COLOR_EDITED)

    @override_settings(OCR_AUTO_OCR=False)
    def test_tag_add_document(self):
        tag = Tag.on_organization.create(
            color=TEST_TAG_COLOR, label=TEST_TAG_LABEL
        )

        document_type = DocumentType.on_organization.create(
            label=TEST_DOCUMENT_TYPE
        )

        with open(TEST_SMALL_DOCUMENT_PATH) as file_object:
            document = document_type.new_document(
                file_object=file_object,
            )

        self.client.post(
            reverse('rest_api:document-tag-list', args=(document.pk,)),
            {'tag': tag.pk}
        )

        self.assertEqual(tag.documents.count(), 1)

    @override_settings(OCR_AUTO_OCR=False)
    def test_tag_remove_document(self):
        tag = Tag.on_organization.create(
            color=TEST_TAG_COLOR, label=TEST_TAG_LABEL
        )

        document_type = DocumentType.on_organization.create(
            label=TEST_DOCUMENT_TYPE
        )

        with open(TEST_SMALL_DOCUMENT_PATH) as file_object:
            document = document_type.new_document(
                file_object=file_object,
            )

        tag.documents.add(document)

        self.client.delete(
            reverse('rest_api:document-tag', args=(document.pk, tag.pk)),
        )

        self.assertEqual(tag.documents.count(), 0)
