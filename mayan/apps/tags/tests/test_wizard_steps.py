from __future__ import unicode_literals

from documents.models import Document
from documents.permissions import permission_document_create
from documents.tests import (
    GenericDocumentViewTestCase, TEST_SMALL_DOCUMENT_PATH,
)
from sources.models import WebFormSource
from sources.tests.literals import (
    TEST_SOURCE_LABEL, TEST_SOURCE_UNCOMPRESS_N
)

from ..models import Tag

from .literals import TEST_TAG_COLOR, TEST_TAG_LABEL, TEST_TAG_LABEL_2


class TaggedDocumentUploadTestCase(GenericDocumentViewTestCase):
    auto_upload_document = False

    def setUp(self):
        super(TaggedDocumentUploadTestCase, self).setUp()
        self.login_user()
        self.source = WebFormSource.objects.create(
            enabled=True, label=TEST_SOURCE_LABEL,
            uncompress=TEST_SOURCE_UNCOMPRESS_N
        )

    def _request_upload_interactive_document_create_view(self):
        with open(TEST_SMALL_DOCUMENT_PATH, mode='rb') as file_object:
            return self.post(
                viewname='sources:upload_interactive', args=(self.source.pk,),
                data={
                    'document_type_id': self.document_type.pk,
                    'source-file': file_object,
                    'tags': ','.join(map(str, Tag.objects.values_list('pk', flat=True)))
                }
            )

    def _create_tag(self):
        self.tag = Tag.objects.create(
            color=TEST_TAG_COLOR, label=TEST_TAG_LABEL
        )

    def _create_tag_2(self):
        self.tag_2 = Tag.objects.create(
            color=TEST_TAG_COLOR, label=TEST_TAG_LABEL_2
        )

    def test_upload_interactive_view_with_access(self):
        self._create_tag()

        self.grant_access(
            permission=permission_document_create, obj=self.document_type
        )
        response = self._request_upload_interactive_document_create_view()
        self.assertEqual(response.status_code, 302)

        self.assertTrue(self.tag in Document.objects.first().tags.all())

    def test_upload_interactive_multiple_tags_view_with_access(self):
        self._create_tag()
        self._create_tag_2()

        self.grant_access(
            permission=permission_document_create, obj=self.document_type
        )
        response = self._request_upload_interactive_document_create_view()
        self.assertEqual(response.status_code, 302)

        self.assertTrue(self.tag in Document.objects.first().tags.all())
        self.assertTrue(self.tag_2 in Document.objects.first().tags.all())
