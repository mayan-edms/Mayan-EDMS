from rest_framework import status

from mayan.apps.documents.permissions import permission_document_type_edit
from mayan.apps.documents.tests.base import DocumentTestMixin
from mayan.apps.rest_api.tests.base import BaseAPITestCase

from ..models import ResolvedWebLink, WebLink
from ..permissions import (
    permission_web_link_create, permission_web_link_delete,
    permission_web_link_edit, permission_web_link_instance_view,
    permission_web_link_view
)

from .literals import TEST_WEB_LINK_LABEL_EDITED, TEST_WEB_LINK_LABEL
from .mixins import (
    ResolvedWebLinkAPIViewTestMixin, WebLinkAPIViewTestMixin, WebLinkTestMixin
)


class WebLinkAPIViewTestCase(
    DocumentTestMixin, WebLinkTestMixin, WebLinkAPIViewTestMixin,
    BaseAPITestCase
):
    auto_create_test_document_type = False
    auto_upload_test_document = False

    def test_web_link_create_view_no_permission(self):
        response = self._request_test_web_link_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertEqual(WebLink.objects.count(), 0)

    def test_web_link_create_view_with_permission(self):
        self.grant_permission(permission=permission_web_link_create)

        response = self._request_test_web_link_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        web_link = WebLink.objects.first()
        self.assertEqual(response.data['id'], web_link.pk)
        self.assertEqual(response.data['label'], TEST_WEB_LINK_LABEL)

        self.assertEqual(WebLink.objects.count(), 1)
        self.assertEqual(web_link.label, TEST_WEB_LINK_LABEL)

    def test_web_link_create_with_document_types_view_no_permission(self):
        self._create_test_document_type()

        response = self._request_test_web_link_create_with_document_type_api_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertEqual(WebLink.objects.count(), 0)

    def test_web_link_create_with_document_types_view_web_link_permission(self):
        self._create_test_document_type()
        self.grant_permission(permission=permission_web_link_create)

        response = self._request_test_web_link_create_with_document_type_api_view()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        web_link = WebLink.objects.first()
        self.assertEqual(response.data['id'], web_link.pk)
        self.assertEqual(response.data['label'], TEST_WEB_LINK_LABEL)

        self.assertEqual(WebLink.objects.count(), 1)
        self.assertEqual(web_link.label, TEST_WEB_LINK_LABEL)
        self.assertTrue(
            self.test_document_type not in web_link.document_types.all()
        )

    def test_web_link_create_with_document_types_view_with_document_type_access(self):
        self._create_test_document_type()
        self.grant_access(
            obj=self.test_document_type, permission=permission_document_type_edit
        )
        response = self._request_test_web_link_create_with_document_type_api_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertEqual(WebLink.objects.count(), 0)

    def test_web_link_create_with_document_types_view_with_full_access(self):
        self._create_test_document_type()
        self.grant_permission(permission=permission_web_link_create)
        self.grant_access(
            obj=self.test_document_type, permission=permission_document_type_edit
        )

        response = self._request_test_web_link_create_with_document_type_api_view()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        web_link = WebLink.objects.first()
        self.assertEqual(response.data['id'], web_link.pk)
        self.assertEqual(response.data['label'], TEST_WEB_LINK_LABEL)

        self.assertEqual(WebLink.objects.count(), 1)
        self.assertEqual(web_link.label, TEST_WEB_LINK_LABEL)
        self.assertTrue(
            self.test_document_type in web_link.document_types.all()
        )

    def test_web_link_delete_view_no_permission(self):
        self._create_test_web_link()

        response = self._request_test_web_link_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(WebLink.objects.count(), 1)

    def test_web_link_delete_view_with_access(self):
        self._create_test_web_link()
        self.grant_access(
            obj=self.test_web_link, permission=permission_web_link_delete
        )

        response = self._request_test_web_link_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(WebLink.objects.count(), 0)

    def test_web_link_detail_view_no_permission(self):
        self._create_test_web_link()

        response = self._request_test_web_link_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertFalse('label' in response.data)

    def test_web_link_detail_view_with_access(self):
        self._create_test_web_link()
        self.grant_access(
            obj=self.test_web_link, permission=permission_web_link_view
        )

        response = self._request_test_web_link_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.data['label'], TEST_WEB_LINK_LABEL
        )

    def test_web_link_edit_view_via_patch_no_permission(self):
        self._create_test_document_type()
        self._create_test_web_link()

        response = self._request_test_web_link_edit_patch_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_web_link.refresh_from_db()
        self.assertEqual(self.test_web_link.label, TEST_WEB_LINK_LABEL)

    def test_web_link_edit_view_via_patch_with_access(self):
        self._create_test_document_type()
        self._create_test_web_link()
        self.grant_access(
            obj=self.test_web_link, permission=permission_web_link_edit
        )

        response = self._request_test_web_link_edit_patch_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_web_link.refresh_from_db()
        self.assertEqual(
            self.test_web_link.label, TEST_WEB_LINK_LABEL_EDITED
        )

    def test_web_link_edit_view_via_put_no_permission(self):
        self._create_test_document_type()
        self._create_test_web_link()

        response = self._request_test_web_link_edit_put_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_web_link.refresh_from_db()
        self.assertEqual(self.test_web_link.label, TEST_WEB_LINK_LABEL)

    def test_web_link_edit_view_via_put_with_access(self):
        self._create_test_document_type()
        self._create_test_web_link()
        self.grant_access(
            obj=self.test_web_link, permission=permission_web_link_edit
        )

        response = self._request_test_web_link_edit_put_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_web_link.refresh_from_db()
        self.assertEqual(
            self.test_web_link.label, TEST_WEB_LINK_LABEL_EDITED
        )


class ResolvedWebLinkAPIViewTestCase(
    DocumentTestMixin, WebLinkTestMixin, ResolvedWebLinkAPIViewTestMixin,
    BaseAPITestCase
):
    def setUp(self):
        super(ResolvedWebLinkAPIViewTestCase, self).setUp()
        self._create_test_web_link(add_document_type=True)

    def test_resolved_web_link_detail_view_no_permission(self):
        response = self._request_resolved_web_link_detail_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_resolved_web_link_detail_view_with_document_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_web_link_instance_view
        )

        response = self._request_resolved_web_link_detail_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_resolved_web_link_detail_view_with_web_link_access(self):
        self.grant_access(
            obj=self.test_web_link,
            permission=permission_web_link_instance_view
        )

        response = self._request_resolved_web_link_detail_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_resolved_web_link_detail_view_with_full_access(self):
        self.grant_access(
            obj=self.test_web_link,
            permission=permission_web_link_instance_view
        )
        self.grant_access(
            obj=self.test_document,
            permission=permission_web_link_instance_view
        )

        response = self._request_resolved_web_link_detail_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['id'], self.test_web_link.pk
        )

    def test_resolved_web_link_list_view_no_permission(self):
        response = self._request_resolved_web_link_list_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertFalse('results' in response.data)

    def test_resolved_web_link_list_view_with_document_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_web_link_instance_view
        )

        response = self._request_resolved_web_link_list_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['count'], 0)

    def test_resolved_web_link_list_view_with_web_link_access(self):
        self.grant_access(
            obj=self.test_web_link,
            permission=permission_web_link_instance_view
        )
        response = self._request_resolved_web_link_list_view()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertFalse('results' in response.data)

    def test_resolved_web_link_list_view_with_full_access(self):
        self.grant_access(
            obj=self.test_web_link,
            permission=permission_web_link_instance_view
        )
        self.grant_access(
            obj=self.test_document,
            permission=permission_web_link_instance_view
        )

        response = self._request_resolved_web_link_list_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['results'][0]['id'], self.test_web_link.pk
        )

    def test_resolved_web_link_navigate_view_no_permission(self):
        response = self._request_resolved_web_link_navigate_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_resolved_web_link_navigate_view_with_web_link_access(self):
        self.grant_access(
            obj=self.test_web_link,
            permission=permission_web_link_instance_view
        )

        response = self._request_resolved_web_link_navigate_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_resolved_web_link_navigate_view_with_document_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_web_link_instance_view
        )
        response = self._request_resolved_web_link_navigate_view()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_resolved_web_link_navigate_view_with_full_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_web_link_instance_view
        )
        self.grant_access(
            obj=self.test_web_link,
            permission=permission_web_link_instance_view
        )

        response = self._request_resolved_web_link_navigate_view()
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(
            response.url, ResolvedWebLink.objects.get(
                pk=self.test_web_link.pk
            ).get_redirect_url_for(document=self.test_document)
        )
