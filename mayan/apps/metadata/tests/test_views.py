from furl import furl

from django.urls import reverse

from mayan.apps.common.settings import setting_home_view
from mayan.apps.documents.permissions import (
    permission_document_properties_edit, permission_document_type_edit,
    permission_document_view
)
from mayan.apps.documents.tests.base import GenericDocumentViewTestCase
from mayan.apps.testing.tests.base import GenericViewTestCase

from ..events import event_metadata_type_relationship_updated
from ..models import MetadataType
from ..permissions import (
    permission_document_metadata_add, permission_document_metadata_remove,
    permission_document_metadata_edit, permission_document_metadata_view,
    permission_metadata_type_create, permission_metadata_type_delete,
    permission_metadata_type_edit, permission_metadata_type_view
)

from .literals import TEST_METADATA_VALUE, TEST_METADATA_VALUE_EDITED
from .mixins import (
    DocumentMetadataMixin, DocumentMetadataViewTestMixin,
    MetadataTypeTestMixin, MetadataTypeViewTestMixin
)


class DocumentMetadataViewTestCase(
    DocumentMetadataMixin, DocumentMetadataViewTestMixin,
    MetadataTypeTestMixin, GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_metadata_type(add_test_document_type=True)
        self._create_test_document_stub()

    def test_document_metadata_add_get_view_no_permission(self):
        document_metadata_count = self.test_document.metadata.count()

        response = self._request_test_document_metadata_add_get_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            self.test_document.metadata.count(), document_metadata_count
        )

    def test_document_metadata_add_get_view_with_document_access(self):
        document_metadata_count = self.test_document.metadata.count()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_metadata_add
        )

        response = self._request_test_document_metadata_add_get_view()
        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            self.test_document.metadata.count(), document_metadata_count
        )

    def test_document_metadata_add_get_view_with_metadata_type_access(self):
        document_metadata_count = self.test_document.metadata.count()

        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_document_metadata_add
        )

        response = self._request_test_document_metadata_add_get_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            self.test_document.metadata.count(), document_metadata_count
        )

    def test_document_metadata_add_get_view_with_full_access(self):
        document_metadata_count = self.test_document.metadata.count()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_metadata_add
        )
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_document_metadata_add
        )

        response = self._request_test_document_metadata_add_get_view()
        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            self.test_document.metadata.count(), document_metadata_count
        )

    def test_trashed_document_metadata_add_get_view_with_full_access(self):
        document_metadata_count = self.test_document.metadata.count()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_metadata_add
        )
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_document_metadata_add
        )

        self.test_document.delete()

        response = self._request_test_document_metadata_add_get_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            self.test_document.metadata.count(), document_metadata_count
        )

    def test_document_metadata_add_post_view_no_permission(self):
        document_metadata_count = self.test_document.metadata.count()

        response = self._request_test_document_metadata_add_post_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            self.test_document.metadata.count(), document_metadata_count
        )

    def test_document_metadata_add_post_view_with_document_access(self):
        document_metadata_count = self.test_document.metadata.count()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_metadata_add
        )

        response = self._request_test_document_metadata_add_post_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self.test_document.metadata.count(), document_metadata_count
        )

    def test_document_metadata_add_post_view_with_metadata_type_access(self):
        document_metadata_count = self.test_document.metadata.count()

        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_document_metadata_add
        )

        response = self._request_test_document_metadata_add_post_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            self.test_document.metadata.count(), document_metadata_count
        )

    def test_document_metadata_add_post_view_with_full_access(self):
        document_metadata_count = self.test_document.metadata.count()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_metadata_add
        )
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_document_metadata_add
        )

        response = self._request_test_document_metadata_add_post_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self.test_document.metadata.count(), document_metadata_count + 1
        )

    def test_trashed_document_metadata_add_post_view_with_full_access(self):
        document_metadata_count = self.test_document.metadata.count()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_metadata_add
        )
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_document_metadata_add
        )

        self.test_document.delete()

        response = self._request_test_document_metadata_add_post_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            self.test_document.metadata.count(), document_metadata_count
        )

    def test_document_metadata_add_redirect(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_metadata_add
        )
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_document_metadata_add
        )

        response = self._request_test_document_metadata_add_post_view()

        self.assertRedirects(
            response=response, expected_url=reverse(
                viewname='metadata:metadata_edit', kwargs={
                    'document_id': self.test_document.pk
                }
            ), status_code=302,
            target_status_code=404
        )

    def test_document_multiple_metadata_add_redirect(self):
        self._create_test_document_stub()

        self.grant_access(
            obj=self.test_documents[0],
            permission=permission_document_metadata_add
        )
        self.grant_access(
            obj=self.test_documents[1],
            permission=permission_document_metadata_add
        )
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_document_metadata_add
        )

        response = self._request_test_document_multiple_metadata_add_post_view()

        url = furl(response.url)

        self.assertEqual(
            url.path, reverse(viewname='metadata:metadata_multiple_edit')
        )

        self.assertEqual(
            set(map(int, url.args['id_list'].split(','))),
            set([self.test_documents[0].pk, self.test_documents[1].pk])
        )

    def test_document_multiple_metadata_add_post_view_with_document_access(self):
        self._create_test_document_stub()

        document_0_metadata_count = self.test_documents[0].metadata.count()
        document_1_metadata_count = self.test_documents[1].metadata.count()

        self.grant_access(
            obj=self.test_documents[0],
            permission=permission_document_metadata_add
        )
        self.grant_access(
            obj=self.test_documents[1],
            permission=permission_document_metadata_add
        )

        response = self._request_test_document_multiple_metadata_add_post_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self.test_documents[0].metadata.count(), document_0_metadata_count
        )
        self.assertEqual(
            self.test_documents[1].metadata.count(), document_1_metadata_count
        )

    def test_document_metadata_multiple_add_post_view_with_full_access(self):
        self._create_test_metadata_type()

        self.test_document_type.metadata.create(
            metadata_type=self.test_metadata_types[1]
        )

        self.grant_permission(permission=permission_document_view)
        self.grant_permission(permission=permission_document_metadata_add)
        self.grant_permission(permission=permission_document_metadata_edit)

        response = self._request_test_document_metadata_multiple_add_post_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self.test_document.metadata.filter(
                metadata_type__in=self._get_test_metadata_type_queryset()
            ).count(), self._get_test_metadata_type_queryset().count()
        )

    def test_document_metadata_edit_post_view_no_permission(self):
        self._create_test_document_metadata()

        document_metadata_value = self.test_document.metadata.first().value

        response = self._request_test_document_metadata_edit_post_view()
        self.assertEqual(response.status_code, 404)

        self.test_document.metadata.first().refresh_from_db()

        self.assertEqual(
            self.test_document.metadata.first().value, document_metadata_value
        )

    def test_document_metadata_edit_post_view_with_document_access(self):
        self._create_test_document_metadata()

        document_metadata_value = self.test_document.metadata.first().value

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_metadata_edit
        )

        response = self._request_test_document_metadata_edit_post_view()
        self.assertEqual(response.status_code, 302)

        self.test_document.metadata.first().refresh_from_db()

        self.assertEqual(
            self.test_document.metadata.first().value, document_metadata_value
        )

    def test_document_metadata_edit_post_view_with_metadata_type_access(self):
        self._create_test_document_metadata()

        document_metadata_value = self.test_document.metadata.first().value

        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_document_metadata_edit
        )

        response = self._request_test_document_metadata_edit_post_view()
        self.assertEqual(response.status_code, 404)

        self.test_document.metadata.first().refresh_from_db()

        self.assertEqual(
            self.test_document.metadata.first().value, document_metadata_value
        )

    def test_document_metadata_edit_post_view_with_full_access(self):
        self._create_test_document_metadata()

        document_metadata_value = self.test_document.metadata.first().value

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_metadata_edit
        )
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_document_metadata_edit
        )

        response = self._request_test_document_metadata_edit_post_view()
        self.assertEqual(response.status_code, 302)

        self.test_document.metadata.first().refresh_from_db()

        self.assertNotEqual(
            self.test_document.metadata.first().value, document_metadata_value
        )

    def test_trashed_document_metadata_edit_post_view_with_full_access(self):
        self._create_test_document_metadata()

        document_metadata_value = self.test_document.metadata.first().value

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_metadata_edit
        )
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_document_metadata_edit
        )

        self.test_document.delete()

        response = self._request_test_document_metadata_edit_post_view()
        self.assertEqual(response.status_code, 404)

        self.test_document.metadata.first().refresh_from_db()

        self.assertEqual(
            self.test_document.metadata.first().value, document_metadata_value
        )

    def test_document_metadata_edit_after_document_type_change(self):
        # Gitlab issue #204
        # Problems to add required metadata after changing the document type

        self.grant_permission(permission=permission_document_properties_edit)
        self.grant_permission(permission=permission_document_metadata_edit)
        self.grant_permission(permission=permission_document_metadata_view)

        self._create_test_document_type()
        self._create_test_metadata_type()

        test_document_metadata_2 = self.test_document_types[1].metadata.create(
            metadata_type=self.test_metadata_types[1], required=True
        )

        self.test_document.document_type_change(
            document_type=self.test_document_types[1]
        )

        response = self.get(
            viewname='metadata:metadata_edit', kwargs={
                'document_id': self.test_document.pk
            }, follow=True
        )
        self.assertContains(response=response, text='Edit', status_code=200)

        response = self._request_test_document_metadata_edit_post_view(
            extra_data={
                'form-0-metadata_type_id': test_document_metadata_2.metadata_type.pk,
            }, follow=True
        )

        self.assertContains(
            response=response, text='Metadata for document', status_code=200
        )

        self.assertEqual(
            self.test_document.metadata.get(
                metadata_type=self.test_metadata_types[1]
            ).value, TEST_METADATA_VALUE_EDITED
        )

    def test_document_metadata_edit_redirect(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_metadata_edit
        )
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_document_metadata_edit
        )

        response = self._request_test_document_metadata_edit_post_view()

        self.assertRedirects(
            response=response, expected_url=reverse(
                viewname='metadata:metadata_view', kwargs={
                    'document_id': self.test_document.pk
                }
            ), status_code=302,
            target_status_code=404
        )

    def test_document_multiple_metadata_edit_redirect(self):
        self._create_test_document_stub()

        self.grant_access(
            obj=self.test_documents[0],
            permission=permission_document_metadata_edit
        )
        self.grant_access(
            obj=self.test_documents[1],
            permission=permission_document_metadata_edit
        )
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_document_metadata_edit
        )

        response = self._request_test_document_multiple_metadata_edit_post_view()
        self.assertEqual(response.status_code, 302)

        url = furl(response.url)
        self.assertEqual(
            url.path, reverse(viewname='metadata:metadata_multiple_edit')
        )

        self.assertEqual(
            set(map(int, url.args['id_list'].split(','))),
            set([self.test_documents[0].pk, self.test_documents[1].pk])
        )

    def test_document_metadata_list_view_no_permission(self):
        self._create_test_document_metadata()

        response = self._request_test_document_metadata_list_view()

        self.assertNotContains(
            response=response, text=self.test_document.label,
            status_code=404
        )
        self.assertNotContains(
            response=response, text=self.test_metadata_type.label,
            status_code=404
        )

    def test_document_metadata_list_view_with_document_access(self):
        self._create_test_document_metadata()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_metadata_view
        )

        response = self._request_test_document_metadata_list_view()

        self.assertContains(
            response=response, text=self.test_document.label,
            status_code=200
        )
        self.assertNotContains(
            response=response, text=self.test_metadata_type.label,
            status_code=200
        )

    def test_document_metadata_list_view_with_metadata_type_access(self):
        self._create_test_document_metadata()

        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_document_metadata_view
        )

        response = self._request_test_document_metadata_list_view()

        self.assertNotContains(
            response=response, text=self.test_document.label,
            status_code=404
        )
        self.assertNotContains(
            response=response, text=self.test_metadata_type.label,
            status_code=404
        )

    def test_document_metadata_list_view_with_full_access(self):
        self._create_test_document_metadata()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_metadata_view
        )
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_document_metadata_view
        )

        response = self._request_test_document_metadata_list_view()

        self.assertContains(
            response=response, text=self.test_document.label,
            status_code=200
        )
        self.assertContains(
            response=response, text=self.test_metadata_type.label,
            status_code=200
        )

    def test_trashed_document_metadata_list_view_with_full_access(self):
        self._create_test_document_metadata()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_metadata_view
        )
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_document_metadata_view
        )

        self.test_document.delete()

        response = self._request_test_document_metadata_list_view()
        self.assertEqual(response.status_code, 404)

    def test_document_metadata_remove_get_view_no_permission(self):
        self._create_test_document_metadata()

        response = self._request_test_document_metadata_remove_get_view()

        self.assertNotContains(
            response=response, text=self.test_metadata_type.label, status_code=404
        )
        self.assertTrue(
            self.test_document_metadata in self.test_document.metadata.all()
        )

    def test_document_metadata_remove_get_view_with_full_access(self):
        self._create_test_document_metadata()

        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_document_metadata_remove,
        )
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_metadata_remove,
        )

        # Silence unrelated logging
        self._silence_logger(name='mayan.apps.navigation.classes')

        response = self._request_test_document_metadata_remove_get_view()
        self.assertContains(
            response, text=self.test_metadata_type.label, status_code=200
        )
        self.assertTrue(
            self.test_document_metadata in self.test_document.metadata.all()
        )

    def test_trashed_document_metadata_remove_get_view_with_full_access(self):
        self._create_test_document_metadata()

        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_document_metadata_remove,
        )
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_metadata_remove,
        )

        # Silence unrelated logging
        self._silence_logger(name='mayan.apps.navigation.classes')

        self.test_document.delete()

        response = self._request_test_document_metadata_remove_get_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            self.test_document_metadata in self.test_document.metadata.all()
        )

    def test_document_metadata_remove_post_view_no_permission(self):
        self._create_test_document_metadata()

        response = self._request_test_document_metadata_remove_get_view()
        self.assertNotContains(
            response=response, text=self.test_metadata_type.label, status_code=404
        )

        self.assertTrue(
            self.test_document_metadata in self.test_document.metadata.all()
        )

    def test_document_metadata_remove_post_view_with_document_access(self):
        self._create_test_document_metadata()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_metadata_remove
        )
        response = self._request_test_document_metadata_remove_post_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            self.test_document_metadata in self.test_document.metadata.all()
        )

    def test_document_metadata_remove_post_view_with_metadata_type_access(self):
        self._create_test_document_metadata()

        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_document_metadata_remove
        )
        response = self._request_test_document_metadata_remove_post_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            self.test_document_metadata in self.test_document.metadata.all()
        )

    def test_document_metadata_remove_post_view_with_full_access(self):
        self._create_test_document_metadata()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_metadata_remove
        )
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_document_metadata_remove
        )
        response = self._request_test_document_metadata_remove_post_view()
        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            self.test_document_metadata not in self.test_document.metadata.all()
        )

    def test_trashed_document_metadata_remove_post_view_with_full_access(self):
        self._create_test_document_metadata()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_metadata_remove
        )
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_document_metadata_remove
        )

        self.test_document.delete()

        response = self._request_test_document_metadata_remove_post_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            self.test_document_metadata in self.test_document.metadata.all()
        )

    def test_document_metadata_remove_redirect(self):
        self._create_test_document_metadata()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_metadata_remove
        )
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_document_metadata_remove
        )

        response = self._request_test_document_metadata_remove_post_view()

        self.assertRedirects(
            response=response, expected_url=reverse(
                viewname='metadata:metadata_view', kwargs={
                    'document_id': self.test_document.pk
                }
            ), status_code=302,
            target_status_code=404
        )

    def test_document_multiple_metadata_remove_redirect(self):
        self._create_test_document_stub()

        self.test_documents[0].metadata.create(
            metadata_type=self.test_metadata_type
        )
        self.test_documents[1].metadata.create(
            metadata_type=self.test_metadata_type
        )

        self.grant_access(
            obj=self.test_documents[0],
            permission=permission_document_metadata_remove
        )
        self.grant_access(
            obj=self.test_documents[1],
            permission=permission_document_metadata_remove
        )
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_document_metadata_remove
        )

        response = self._request_test_document_multiple_metadata_remove_post_view()
        self.assertRedirects(
            response=response, expected_url=reverse(
                viewname=setting_home_view.value
            ), status_code=302,
            target_status_code=200
        )

    def test_document_multiple_metadata_remove_view_with_access(self):
        self.grant_permission(permission=permission_document_view)
        self.grant_permission(permission=permission_document_metadata_remove)

        self._create_test_document_stub()

        self.test_documents[0].metadata.create(
            metadata_type=self.test_metadata_type
        )
        self.test_documents[1].metadata.create(
            metadata_type=self.test_metadata_type
        )

        response = self._request_test_document_multiple_metadata_remove_get_view()
        self.assertEqual(response.status_code, 200)

        # Test post to metadata removal view
        response = self._request_test_document_multiple_metadata_remove_post_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(self.test_documents[0].metadata.count(), 0)
        self.assertEqual(self.test_documents[1].metadata.count(), 0)

    def test_multiple_document_metadata_edit(self):
        self._create_test_document_stub()

        self.grant_permission(permission=permission_document_view)
        self.grant_permission(permission=permission_document_metadata_add)
        self.grant_permission(permission=permission_document_metadata_edit)

        self.test_documents[0].metadata.create(
            metadata_type=self.test_metadata_type
        )
        self.test_documents[1].metadata.create(
            metadata_type=self.test_metadata_type
        )

        response = self._request_test_document_multiple_metadata_edit_get_view()
        self.assertContains(response=response, text='Edit', status_code=200)

        # Test post to metadata removal view
        response = self._request_test_document_multiple_metadata_edit_post_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self.test_documents[0].metadata.first().value,
            TEST_METADATA_VALUE_EDITED
        )
        self.assertEqual(
            self.test_documents[1].metadata.first().value,
            TEST_METADATA_VALUE_EDITED
        )


class DocumentMetadataRequiredTestCase(
    DocumentMetadataViewTestMixin, MetadataTypeTestMixin,
    GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_metadata_type(add_test_document_type=True)
        self._create_test_metadata_type(
            add_test_document_type=True, required=True
        )
        self._create_test_document_stub()

    def _create_test_document_metadata(self):
        self.test_document.metadata.update_or_create(
            metadata_type=self.test_metadata_types[0],
            defaults={'value': TEST_METADATA_VALUE}
        )

        self.test_document.metadata.update_or_create(
            metadata_type=self.test_metadata_types[1],
            defaults={'value': TEST_METADATA_VALUE}
        )

    def test_document_metadata_remove_post_view_with_access_non_required_from_dual(self):
        # Adds two metadata types to the document type: one required and
        # one optional. Add both to a document. Attempts to remove the optional
        # one.
        self._create_test_document_metadata()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_metadata_remove
        )
        self.grant_access(
            obj=self.test_metadata_types[0],
            permission=permission_document_metadata_remove
        )
        self.grant_access(
            obj=self.test_metadata_types[1],
            permission=permission_document_metadata_remove
        )

        response = self._request_test_document_metadata_remove_post_view(index=0)
        self.assertEqual(response.status_code, 302)

        self.assertFalse(
            self.test_document.metadata.filter(
                metadata_type=self.test_metadata_types[0]
            ).exists()
        )
        self.assertTrue(
            self.test_document.metadata.filter(
                metadata_type=self.test_metadata_types[1]
            ).exists()
        )

    def test_document_metadata_remove_post_view_with_access_required_from_dual(self):
        # Adds two metadata types to the document type: one required and
        # one optional. Add both to a document. Attempts to remove the required
        # one.
        self._create_test_document_metadata()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_metadata_remove
        )
        self.grant_access(
            obj=self.test_metadata_types[0],
            permission=permission_document_metadata_remove
        )
        self.grant_access(
            obj=self.test_metadata_types[1],
            permission=permission_document_metadata_remove
        )

        response = self._request_test_document_metadata_remove_post_view(index=1)
        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            self.test_document.metadata.filter(
                metadata_type=self.test_metadata_types[0]
            ).exists()
        )
        self.assertTrue(
            self.test_document.metadata.filter(
                metadata_type=self.test_metadata_types[1]
            ).exists()
        )

    def test_document_multiple_metadata_edit_mixed_required_non_selection_required_view(self):
        # Tried to edit the multiple metadata from two documents, deselecting
        # the update checkmark from the required metadata which already has
        # a value. GitLab issue #936
        # "Bulk editing of metadata: error when "update" option of a required field is unchecked"
        self._create_test_document_metadata()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_metadata_edit
        )
        self.grant_access(
            obj=self.test_metadata_types[0],
            permission=permission_document_metadata_edit
        )
        self.grant_access(
            obj=self.test_metadata_types[1],
            permission=permission_document_metadata_edit
        )

        response = self._request_test_document_metadata_edit_post_view(
            extra_data={
                'form-0-metadata_type_id': self._test_document_type_metadata_type_relationships[0].metadata_type.pk,
                'form-0-update': True,
                'form-0-value': TEST_METADATA_VALUE_EDITED,
                'form-1-metadata_type_id': self._test_document_type_metadata_type_relationships[1].metadata_type.pk,  # Required
                'form-1-update': False,
                'form-1-value': TEST_METADATA_VALUE_EDITED,
                'form-TOTAL_FORMS': '2',
                'form-INITIAL_FORMS': '0',
                'form-MAX_NUM_FORMS': '',
            }
        )
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self.test_document.metadata.get(
                metadata_type=self.test_metadata_types[0],
            ).value, TEST_METADATA_VALUE_EDITED
        )
        self.assertEqual(
            self.test_document.metadata.get(
                metadata_type=self.test_metadata_types[1],
            ).value, TEST_METADATA_VALUE
        )


class DocumentTypeMetadataTypeRelationshipViewTestCase(
    MetadataTypeViewTestMixin, MetadataTypeTestMixin,
    GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_metadata_type()

    def test_document_type_relationship_delete_view_no_permission(self):
        self.test_document_type.metadata.create(
            metadata_type=self.test_metadata_type
        )

        test_document_type_metadata_type_relationship_count = self.test_document_type.metadata.count()

        self._clear_events()

        response = self._request_test_document_type_relationship_delete_view()
        self.assertEqual(response.status_code, 404)

        self.test_document_type.refresh_from_db()
        self.assertEqual(
            self.test_document_type.metadata.count(),
            test_document_type_metadata_type_relationship_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_relationship_delete_view_with_metadata_type_access(self):
        self.test_document_type.metadata.create(
            metadata_type=self.test_metadata_type
        )

        test_document_type_metadata_type_relationship_count = self.test_document_type.metadata.count()

        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_metadata_type_edit
        )

        self._clear_events()

        response = self._request_test_document_type_relationship_delete_view()
        self.assertEqual(response.status_code, 404)

        self.test_document_type.refresh_from_db()
        self.assertEqual(
            self.test_document_type.metadata.count(),
            test_document_type_metadata_type_relationship_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_relationship_delete_view_with_document_type_access(self):
        self.test_document_type.metadata.create(
            metadata_type=self.test_metadata_type
        )

        test_document_type_metadata_type_relationship_count = self.test_document_type.metadata.count()

        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )

        self._clear_events()

        response = self._request_test_document_type_relationship_delete_view()
        self.assertEqual(response.status_code, 302)

        self.test_document_type.refresh_from_db()
        self.assertEqual(
            self.test_document_type.metadata.count(),
            test_document_type_metadata_type_relationship_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_relationship_delete_view_with_full_access(self):
        self.test_document_type.metadata.create(
            metadata_type=self.test_metadata_type
        )

        test_document_type_metadata_type_relationship_count = self.test_document_type.metadata.count()

        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_metadata_type_edit
        )

        self._clear_events()

        response = self._request_test_document_type_relationship_delete_view()
        self.assertEqual(response.status_code, 302)

        self.test_document_type.refresh_from_db()
        self.assertEqual(
            self.test_document_type.metadata.count(),
            test_document_type_metadata_type_relationship_count - 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self.test_metadata_type)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_document_type)
        self.assertEqual(events[0].verb, event_metadata_type_relationship_updated.id)

    def test_document_type_relationship_edit_view_no_permission(self):
        test_document_type_metadata_type_relationship_count = self.test_document_type.metadata.count()

        self._clear_events()

        response = self._request_test_document_type_relationship_edit_view()
        self.assertEqual(response.status_code, 404)

        self.test_document_type.refresh_from_db()
        self.assertEqual(
            self.test_document_type.metadata.count(),
            test_document_type_metadata_type_relationship_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_relationship_edit_view_with_metadata_type_access(self):
        test_document_type_metadata_type_relationship_count = self.test_document_type.metadata.count()

        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_metadata_type_edit
        )

        self._clear_events()

        response = self._request_test_document_type_relationship_edit_view()
        self.assertEqual(response.status_code, 404)

        self.test_document_type.refresh_from_db()
        self.assertEqual(
            self.test_document_type.metadata.count(),
            test_document_type_metadata_type_relationship_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_relationship_edit_view_with_document_type_access(self):
        test_document_type_metadata_type_relationship_count = self.test_document_type.metadata.count()

        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )

        self._clear_events()

        response = self._request_test_document_type_relationship_edit_view()
        self.assertEqual(response.status_code, 302)

        self.test_document_type.refresh_from_db()
        self.assertEqual(
            self.test_document_type.metadata.count(),
            test_document_type_metadata_type_relationship_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_relationship_edit_view_with_full_access(self):
        test_document_type_metadata_type_relationship_count = self.test_document_type.metadata.count()

        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_metadata_type_edit
        )

        self._clear_events()

        response = self._request_test_document_type_relationship_edit_view()
        self.assertEqual(response.status_code, 302)

        self.test_document_type.refresh_from_db()
        self.assertEqual(
            self.test_document_type.metadata.count(),
            test_document_type_metadata_type_relationship_count + 1
        )

        self.assertQuerysetEqual(
            qs=self.test_document_type.metadata.values(
                'metadata_type', 'required'
            ),
            values=[
                {
                    'metadata_type': self.test_metadata_type.pk,
                    'required': True,
                }
            ], transform=dict
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self.test_metadata_type)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_document_type)
        self.assertEqual(events[0].verb, event_metadata_type_relationship_updated.id)


class MetadataTypeViewTestCase(
    MetadataTypeViewTestMixin, MetadataTypeTestMixin, GenericViewTestCase
):
    def test_metadata_type_create_view_no_permission(self):
        metadata_type_count = MetadataType.objects.count()

        response = self._request_test_metadata_type_create_view()
        self.assertEqual(response.status_code, 403)

        self.assertEqual(
            MetadataType.objects.count(), metadata_type_count
        )

    def test_metadata_type_create_view_with_access(self):
        self.grant_permission(permission=permission_metadata_type_create)
        metadata_type_count = MetadataType.objects.count()

        response = self._request_test_metadata_type_create_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            MetadataType.objects.count(), metadata_type_count + 1
        )

    def test_metadata_type_delete_view_no_permission(self):
        self._create_test_metadata_type()
        metadata_type_count = MetadataType.objects.count()

        response = self._request_test_metadata_type_delete_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            MetadataType.objects.count(), metadata_type_count
        )

    def test_metadata_type_delete_view_with_access(self):
        self._create_test_metadata_type()

        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_metadata_type_delete
        )
        metadata_type_count = MetadataType.objects.count()

        response = self._request_test_metadata_type_delete_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            MetadataType.objects.count(), metadata_type_count - 1
        )

    def test_metadata_type_edit_view_no_permission(self):
        self._create_test_metadata_type()
        metadata_type_values = self._model_instance_to_dictionary(
            instance=self.test_metadata_type
        )

        response = self._request_test_metadata_type_edit_view()
        self.assertEqual(response.status_code, 404)

        self.test_metadata_type.refresh_from_db()
        self.assertEqual(
            self._model_instance_to_dictionary(
                instance=self.test_metadata_type
            ), metadata_type_values
        )

    def test_metadata_type_edit_view_with_access(self):
        self._create_test_metadata_type()

        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_metadata_type_edit
        )
        metadata_type_values = self._model_instance_to_dictionary(
            instance=self.test_metadata_type
        )

        response = self._request_test_metadata_type_edit_view()
        self.assertEqual(response.status_code, 302)

        self.test_metadata_type.refresh_from_db()
        self.assertNotEqual(
            self._model_instance_to_dictionary(
                instance=self.test_metadata_type
            ), metadata_type_values
        )

    def test_metadata_type_list_view_no_permission(self):
        self._create_test_metadata_type()

        response = self._request_metadata_type_list_view()
        self.assertNotContains(
            response=response, text=self.test_metadata_type, status_code=200
        )

    def test_metadata_type_list_view_with_access(self):
        self._create_test_metadata_type()

        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_metadata_type_view
        )

        response = self._request_metadata_type_list_view()
        self.assertContains(
            response=response, text=self.test_metadata_type, status_code=200
        )


class MetadataTypeDocumentTypeRelationshipViewTestCase(
    MetadataTypeViewTestMixin, MetadataTypeTestMixin,
    GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_metadata_type()

    def test_metadata_type_relationship_delete_view_no_permission(self):
        self.test_metadata_type.document_types.create(
            document_type=self.test_document_type
        )

        test_metadata_type_document_type_relationship_count = self.test_metadata_type.document_types.count()

        self._clear_events()

        response = self._request_test_metadata_type_document_type_relationship_delete_view()
        self.assertEqual(response.status_code, 404)

        self.test_metadata_type.refresh_from_db()
        self.assertEqual(
            self.test_metadata_type.document_types.count(),
            test_metadata_type_document_type_relationship_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_metadata_type_relationship_delete_view_with_document_type_access(self):
        self.test_metadata_type.document_types.create(
            document_type=self.test_document_type
        )

        test_metadata_type_document_type_relationship_count = self.test_metadata_type.document_types.count()

        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )

        self._clear_events()

        response = self._request_test_metadata_type_document_type_relationship_delete_view()
        self.assertEqual(response.status_code, 404)

        self.test_metadata_type.refresh_from_db()
        self.assertEqual(
            self.test_metadata_type.document_types.count(),
            test_metadata_type_document_type_relationship_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_metadata_type_relationship_delete_view_with_metadata_type_access(self):
        self.test_metadata_type.document_types.create(
            document_type=self.test_document_type
        )

        test_metadata_type_document_type_relationship_count = self.test_metadata_type.document_types.count()

        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_metadata_type_edit
        )

        self._clear_events()

        response = self._request_test_metadata_type_document_type_relationship_delete_view()
        self.assertEqual(response.status_code, 302)

        self.test_metadata_type.refresh_from_db()
        self.assertEqual(
            self.test_metadata_type.document_types.count(),
            test_metadata_type_document_type_relationship_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_metadata_type_relationship_delete_view_with_full_access(self):
        self.test_metadata_type.document_types.create(
            document_type=self.test_document_type
        )

        test_metadata_type_document_type_relationship_count = self.test_metadata_type.document_types.count()

        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_metadata_type_edit
        )
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )

        self._clear_events()

        response = self._request_test_metadata_type_document_type_relationship_delete_view()
        self.assertEqual(response.status_code, 302)

        self.test_metadata_type.refresh_from_db()
        self.assertEqual(
            self.test_metadata_type.document_types.count(),
            test_metadata_type_document_type_relationship_count - 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self.test_metadata_type)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_document_type)
        self.assertEqual(events[0].verb, event_metadata_type_relationship_updated.id)

    def test_metadata_type_document_type_relationship_view_no_permission(self):
        test_metadata_type_document_type_relationship_count = self.test_metadata_type.document_types.count()

        self._clear_events()

        response = self._request_test_metadata_type_document_type_relationship_edit_view()
        self.assertEqual(response.status_code, 404)

        self.test_document_type.refresh_from_db()
        self.assertEqual(
            self.test_metadata_type.document_types.count(),
            test_metadata_type_document_type_relationship_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_metadata_type_document_type_relationship_view_with_document_type_access(self):
        test_metadata_type_document_type_relationship_count = self.test_metadata_type.document_types.count()

        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )

        self._clear_events()

        response = self._request_test_metadata_type_document_type_relationship_edit_view()
        self.assertEqual(response.status_code, 404)

        self.test_document_type.refresh_from_db()
        self.assertEqual(
            self.test_metadata_type.document_types.count(),
            test_metadata_type_document_type_relationship_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_metadata_type_document_type_relationship_view_with_metadata_type_access(self):
        test_metadata_type_document_type_relationship_count = self.test_metadata_type.document_types.count()

        self.grant_access(
            obj=self.test_metadata_type, permission=permission_metadata_type_edit
        )

        self._clear_events()

        response = self._request_test_metadata_type_document_type_relationship_edit_view()
        self.assertEqual(response.status_code, 302)

        self.test_document_type.refresh_from_db()
        self.assertEqual(
            self.test_metadata_type.document_types.count(),
            test_metadata_type_document_type_relationship_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_metadata_type_document_type_relationship_view_with_full_access(self):
        test_metadata_type_document_type_relationship_count = self.test_metadata_type.document_types.count()

        self.grant_access(
            obj=self.test_metadata_type, permission=permission_metadata_type_edit
        )
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )

        self._clear_events()

        response = self._request_test_metadata_type_document_type_relationship_edit_view()
        self.assertEqual(response.status_code, 302)

        self.test_document_type.refresh_from_db()
        self.assertEqual(
            self.test_metadata_type.document_types.count(),
            test_metadata_type_document_type_relationship_count + 1
        )

        self.assertQuerysetEqual(
            qs=self.test_document_type.metadata.values(
                'metadata_type', 'required'
            ),
            values=[
                {
                    'metadata_type': self.test_metadata_type.pk,
                    'required': True,
                }
            ], transform=dict
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self.test_metadata_type)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_document_type)
        self.assertEqual(events[0].verb, event_metadata_type_relationship_updated.id)
