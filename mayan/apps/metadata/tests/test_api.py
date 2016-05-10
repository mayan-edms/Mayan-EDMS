from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import override_settings

from rest_framework.test import APITestCase

from documents.models import DocumentType
from documents.tests import TEST_DOCUMENT_TYPE, TEST_SMALL_DOCUMENT_PATH
from user_management.tests.literals import (
    TEST_ADMIN_EMAIL, TEST_ADMIN_PASSWORD, TEST_ADMIN_USERNAME
)

from ..models import DocumentMetadata, DocumentTypeMetadataType, MetadataType

from .literals import (
    TEST_METADATA_TYPE_LABEL, TEST_METADATA_TYPE_LABEL_2,
    TEST_METADATA_TYPE_NAME, TEST_METADATA_TYPE_NAME_2
)


class MetadataTypeAPITestCase(APITestCase):
    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(
            username=TEST_ADMIN_USERNAME, email=TEST_ADMIN_EMAIL,
            password=TEST_ADMIN_PASSWORD
        )

        self.client.login(
            username=TEST_ADMIN_USERNAME, password=TEST_ADMIN_PASSWORD
        )

    def tearDown(self):
        self.admin_user.delete()

    def test_metadata_type_create(self):
        response = self.client.post(
            reverse('rest_api:metadatatype-list'), data={
                'label': TEST_METADATA_TYPE_LABEL,
                'name': TEST_METADATA_TYPE_NAME
            }
        )

        metadata_type = MetadataType.objects.first()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['id'], metadata_type.pk)
        self.assertEqual(response.data['label'], TEST_METADATA_TYPE_LABEL)
        self.assertEqual(response.data['name'], TEST_METADATA_TYPE_NAME)

        self.assertEqual(metadata_type.label, TEST_METADATA_TYPE_LABEL)
        self.assertEqual(metadata_type.name, TEST_METADATA_TYPE_NAME)

    def test_metadata_type_delete(self):
        metadata_type = MetadataType.objects.create(
            label=TEST_METADATA_TYPE_LABEL, name=TEST_METADATA_TYPE_NAME
        )

        response = self.client.delete(
            reverse('rest_api:metadatatype-detail', args=(metadata_type.pk,))
        )

        self.assertEqual(response.status_code, 204)

        self.assertEqual(MetadataType.objects.count(), 0)

    def test_metadata_type_edit(self):
        metadata_type = MetadataType.objects.create(
            label=TEST_METADATA_TYPE_LABEL, name=TEST_METADATA_TYPE_NAME
        )

        response = self.client.put(
            reverse('rest_api:metadatatype-detail', args=(metadata_type.pk,)),
            data={
                'label': TEST_METADATA_TYPE_LABEL_2,
                'name': TEST_METADATA_TYPE_NAME_2
            }
        )

        self.assertEqual(response.status_code, 200)

        metadata_type.refresh_from_db()

        self.assertEqual(metadata_type.label, TEST_METADATA_TYPE_LABEL_2)
        self.assertEqual(metadata_type.name, TEST_METADATA_TYPE_NAME_2)


class DocumentTypeMetadataTypeAPITestCase(APITestCase):
    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(
            username=TEST_ADMIN_USERNAME, email=TEST_ADMIN_EMAIL,
            password=TEST_ADMIN_PASSWORD
        )

        self.client.login(
            username=TEST_ADMIN_USERNAME, password=TEST_ADMIN_PASSWORD
        )

        self.document_type = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE
        )

        self.metadata_type = MetadataType.objects.create(
            label=TEST_METADATA_TYPE_LABEL, name=TEST_METADATA_TYPE_NAME
        )

    def tearDown(self):
        self.admin_user.delete()
        self.document_type.delete()

    def test_document_type_metadata_type_optional_create(self):
        response = self.client.post(
            reverse(
                'rest_api:documenttypeoptionalmetadatatype-list',
                args=(self.document_type.pk,)
            ), data={'metadata_type_pk': self.metadata_type.pk}
        )

        self.assertEqual(response.status_code, 201)

        document_type_metadata_type = DocumentTypeMetadataType.objects.filter(document_type=self.document_type, required=False).first()

        self.assertEqual(response.data['pk'], document_type_metadata_type.pk)

        self.assertEqual(
            document_type_metadata_type.metadata_type, self.metadata_type
        )

    def test_document_type_metadata_type_required_create(self):
        response = self.client.post(
            reverse(
                'rest_api:documenttyperequiredmetadatatype-list',
                args=(self.document_type.pk,)
            ), data={'metadata_type_pk': self.metadata_type.pk}
        )

        self.assertEqual(response.status_code, 201)

        document_type_metadata_type = DocumentTypeMetadataType.objects.filter(document_type=self.document_type, required=True).first()

        self.assertEqual(response.data['pk'], document_type_metadata_type.pk)

        self.assertEqual(
            document_type_metadata_type.metadata_type, self.metadata_type
        )


    def test_document_type_metadata_type_required_create(self):
        response = self.client.post(
            reverse(
                'rest_api:documenttyperequiredmetadatatype-list',
                args=(self.document_type.pk,)
            ), data={'metadata_type_pk': self.metadata_type.pk}
        )

        self.assertEqual(response.status_code, 201)

        document_type_metadata_type = DocumentTypeMetadataType.objects.filter(document_type=self.document_type, required=True).first()

        self.assertEqual(response.data['pk'], document_type_metadata_type.pk)

        self.assertEqual(
            document_type_metadata_type.metadata_type, self.metadata_type
        )

    def test_document_type_metadata_type_delete(self):
        document_type_metadata_type = self.document_type.metadata.create(
            metadata_type=self.metadata_type, required=True
        )

        response = self.client.delete(
            reverse(
                'rest_api:documenttypemetadatatype-detail',
                args=(document_type_metadata_type.pk,)
            ),
        )

        self.assertEqual(response.status_code, 204)

        self.assertEqual(self.document_type.metadata.all().count(), 0)
