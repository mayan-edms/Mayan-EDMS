from __future__ import absolute_import, unicode_literals

from mayan.apps.common.tests import GenericViewTestCase
from mayan.apps.documents.permissions import permission_document_view
from mayan.apps.documents.tests import GenericDocumentViewTestCase

from ..models import SmartLink
from ..permissions import (
    permission_smart_link_create, permission_smart_link_delete,
    permission_smart_link_edit, permission_smart_link_view
)

from .literals import (
    TEST_SMART_LINK_DYNAMIC_LABEL, TEST_SMART_LINK_LABEL_EDITED,
    TEST_SMART_LINK_LABEL
)
from .mixins import SmartLinkTestMixin


class SmartLinkViewTestCase(SmartLinkTestMixin, GenericViewTestCase):
    def _request_test_smart_link_create_view(self):
        return self.post(
            viewname='linking:smart_link_create', data={
                'label': TEST_SMART_LINK_LABEL
            }
        )

    def test_smart_link_create_view_no_permission(self):
        response = self._request_test_smart_link_create_view()
        self.assertEquals(response.status_code, 403)

        self.assertEqual(SmartLink.objects.count(), 0)

    def test_smart_link_create_view_with_permission(self):
        self.grant_permission(permission=permission_smart_link_create)

        response = self._request_test_smart_link_create_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(SmartLink.objects.count(), 1)
        self.assertEqual(
            SmartLink.objects.first().label, TEST_SMART_LINK_LABEL
        )

    def _request_test_smart_link_delete_view(self):
        return self.post(
            viewname='linking:smart_link_delete', kwargs={
                'pk': self.test_smart_link.pk
            }
        )

    def test_smart_link_delete_view_no_permission(self):
        self._create_test_smart_link()

        response = self._request_test_smart_link_delete_view()
        self.assertEqual(response.status_code, 403)

        self.assertEqual(SmartLink.objects.count(), 1)

    def test_smart_link_delete_view_with_permission(self):
        self._create_test_smart_link()
        self.grant_permission(permission=permission_smart_link_delete)

        response = self._request_test_smart_link_delete_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(SmartLink.objects.count(), 0)

    def _request_test_smart_link_edit_view(self):
        return self.post(
            viewname='linking:smart_link_edit', kwargs={
                'pk': self.test_smart_link.pk
            }, data={
                'label': TEST_SMART_LINK_LABEL_EDITED
            }
        )

    def test_smart_link_edit_view_no_permission(self):
        self._create_test_smart_link()

        response = self._request_test_smart_link_edit_view()
        self.assertEqual(response.status_code, 403)

        self.test_smart_link.refresh_from_db()
        self.assertEqual(self.test_smart_link.label, TEST_SMART_LINK_LABEL)

    def test_smart_link_edit_view_with_permission(self):
        self._create_test_smart_link()

        self.grant_permission(permission=permission_smart_link_edit)

        response = self._request_test_smart_link_edit_view()
        self.assertEqual(response.status_code, 302)

        self.test_smart_link.refresh_from_db()
        self.assertEqual(self.test_smart_link.label, TEST_SMART_LINK_LABEL_EDITED)


class SmartLinkDocumentViewTestCase(SmartLinkTestMixin, GenericDocumentViewTestCase):
    def setup_smart_links(self):
        self.test_smart_link = SmartLink.objects.create(
            label=TEST_SMART_LINK_LABEL,
            dynamic_label=TEST_SMART_LINK_DYNAMIC_LABEL
        )
        self.test_smart_link.document_types.add(self.test_document_type)

        self.test_smart_link_2 = SmartLink.objects.create(
            label=TEST_SMART_LINK_LABEL,
            dynamic_label=TEST_SMART_LINK_DYNAMIC_LABEL
        )
        self.test_smart_link_2.document_types.add(self.test_document_type)

    def _request_test_smart_link_document_instances_view(self):
        return self.get(
            viewname='linking:smart_link_instances_for_document',
            kwargs={'pk': self.test_document.pk}
        )

    def test_document_smart_link_list_view_no_permission(self):
        self.setup_smart_links()

        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        response = self._request_test_smart_link_document_instances_view()
        # Text must appear 2 times, only for the windows title and template
        # heading. The two smart links are not shown.
        self.assertContains(
            response, text=self.test_document.label, count=2, status_code=200
        )

    def test_document_smart_link_list_view_with_permission(self):
        self.setup_smart_links()

        self.grant_access(
            obj=self.test_smart_link, permission=permission_smart_link_view
        )
        self.grant_access(
            obj=self.test_smart_link_2, permission=permission_smart_link_view
        )
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        response = self._request_test_smart_link_document_instances_view()
        # Text must appear 4 times: 2 for the windows title and template
        # heading, plus 2 for the test.
        self.assertContains(
            response, text=self.test_document.label, count=4, status_code=200
        )
