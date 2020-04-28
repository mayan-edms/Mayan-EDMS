from mayan.apps.common.tests.base import GenericViewTestCase
from mayan.apps.documents.permissions import permission_document_view
from mayan.apps.documents.tests.base import GenericDocumentViewTestCase

from ..models import SmartLink
from ..permissions import (
    permission_smart_link_create, permission_smart_link_delete,
    permission_smart_link_edit, permission_smart_link_view
)

from .literals import TEST_SMART_LINK_LABEL, TEST_SMART_LINK_LABEL_EDITED
from .mixins import (
    SmartLinkConditionViewTestMixin, SmartLinkDocumentViewTestMixin,
    SmartLinkTestMixin, SmartLinkViewTestMixin
)


class SmartLinkViewTestCase(
    SmartLinkTestMixin, SmartLinkViewTestMixin, GenericViewTestCase
):
    def test_smart_link_create_view_no_permission(self):
        response = self._request_test_smart_link_create_view()
        self.assertEqual(response.status_code, 403)

        self.assertEqual(SmartLink.objects.count(), 0)

    def test_smart_link_create_view_with_permission(self):
        self.grant_permission(permission=permission_smart_link_create)

        response = self._request_test_smart_link_create_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(SmartLink.objects.count(), 1)
        self.assertEqual(
            SmartLink.objects.first().label, TEST_SMART_LINK_LABEL
        )

    def test_smart_link_delete_view_no_permission(self):
        self._create_test_smart_link()

        response = self._request_test_smart_link_delete_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(SmartLink.objects.count(), 1)

    def test_smart_link_delete_view_with_access(self):
        self._create_test_smart_link()
        self.grant_access(
            obj=self.test_smart_link, permission=permission_smart_link_delete
        )

        response = self._request_test_smart_link_delete_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(SmartLink.objects.count(), 0)

    def test_smart_link_edit_view_no_permission(self):
        self._create_test_smart_link()

        response = self._request_test_smart_link_edit_view()
        self.assertEqual(response.status_code, 404)

        self.test_smart_link.refresh_from_db()
        self.assertEqual(self.test_smart_link.label, TEST_SMART_LINK_LABEL)

    def test_smart_link_edit_view_with_access(self):
        self._create_test_smart_link()

        self.grant_access(
            obj=self.test_smart_link, permission=permission_smart_link_edit
        )

        response = self._request_test_smart_link_edit_view()
        self.assertEqual(response.status_code, 302)

        self.test_smart_link.refresh_from_db()
        self.assertEqual(
            self.test_smart_link.label, TEST_SMART_LINK_LABEL_EDITED
        )


class SmartLinkConditionViewTestCase(
    SmartLinkConditionViewTestMixin, SmartLinkTestMixin,
    SmartLinkViewTestMixin, GenericViewTestCase
):
    def test_smart_link_condition_create_view_no_permission(self):
        self._create_test_smart_link()

        condition_count = self.test_smart_link.conditions.count()

        response = self._request_test_smart_link_condition_create_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            self.test_smart_link.conditions.count(), condition_count
        )

    def test_smart_link_condition_create_view_with_access(self):
        self._create_test_smart_link()
        self.grant_access(
            obj=self.test_smart_link, permission=permission_smart_link_edit
        )

        condition_count = self.test_smart_link.conditions.count()

        response = self._request_test_smart_link_condition_create_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self.test_smart_link.conditions.count(), condition_count + 1
        )

    def test_smart_link_condition_list_view_no_permission(self):
        self._create_test_smart_link()
        self._create_test_smart_link_condition()

        response = self._request_test_smart_link_condition_list_view()
        self.assertNotContains(
            response=response, status_code=404,
            text=self.test_smart_link_condition.smart_link.label
        )

    def test_smart_link_condition_list_view_with_access(self):
        self._create_test_smart_link()
        self._create_test_smart_link_condition()
        self.grant_access(
            obj=self.test_smart_link, permission=permission_smart_link_edit
        )

        response = self._request_test_smart_link_condition_list_view()
        self.assertContains(
            response=response, status_code=200,
            text=self.test_smart_link_condition.smart_link.label
        )

    def test_smart_link_condition_delete_view_no_permission(self):
        self._create_test_smart_link()
        self._create_test_smart_link_condition()
        condition_count = self.test_smart_link.conditions.count()

        response = self._request_test_smart_link_condition_delete_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            self.test_smart_link.conditions.count(), condition_count
        )

    def test_smart_link_condition_delete_view_with_access(self):
        self._create_test_smart_link()
        self._create_test_smart_link_condition()
        self.grant_access(
            obj=self.test_smart_link, permission=permission_smart_link_edit
        )
        condition_count = self.test_smart_link.conditions.count()

        response = self._request_test_smart_link_condition_delete_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self.test_smart_link.conditions.count(), condition_count - 1
        )

    def test_smart_link_condition_edit_view_no_permission(self):
        self._create_test_smart_link()
        self._create_test_smart_link_condition()
        instance_values = self._model_instance_to_dictionary(
            instance=self.test_smart_link_condition
        )

        response = self._request_test_smart_link_condition_edit_view()
        self.assertEqual(response.status_code, 404)

        self.test_smart_link_condition.refresh_from_db()
        self.assertEqual(
            self._model_instance_to_dictionary(
                instance=self.test_smart_link_condition
            ), instance_values
        )

    def test_smart_link_condition_edit_view_with_access(self):
        self._create_test_smart_link()
        self._create_test_smart_link_condition()
        self.grant_access(
            obj=self.test_smart_link, permission=permission_smart_link_edit
        )
        instance_values = self._model_instance_to_dictionary(
            instance=self.test_smart_link_condition
        )

        response = self._request_test_smart_link_condition_edit_view()
        self.assertEqual(response.status_code, 302)

        self.test_smart_link_condition.refresh_from_db()
        self.assertNotEqual(
            self._model_instance_to_dictionary(
                instance=self.test_smart_link_condition
            ), instance_values
        )


class SmartLinkDocumentViewTestCase(
    SmartLinkTestMixin, SmartLinkDocumentViewTestMixin,
    GenericDocumentViewTestCase
):
    def setUp(self):
        super(SmartLinkDocumentViewTestCase, self).setUp()
        self._create_test_smart_links(add_test_document_type=True)

    def test_document_smart_link_list_view_no_permission(self):
        response = self._request_test_smart_link_document_instances_view()
        self.assertNotContains(
            response=response, status_code=404, text=self.test_document.label
        )

    def test_document_smart_link_list_view_with_document_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        response = self._request_test_smart_link_document_instances_view()
        # Text must appear 3 times, two for the title and one for the template
        # heading. The two smart links are not shown.
        self.assertContains(
            count=3, response=response, status_code=200,
            text=self.test_document.label
        )

    def test_document_smart_link_list_view_with_smart_link_access(self):
        self.grant_access(
            obj=self.test_smart_links[0],
            permission=permission_smart_link_view
        )
        self.grant_access(
            obj=self.test_smart_links[1],
            permission=permission_smart_link_view
        )

        response = self._request_test_smart_link_document_instances_view()
        self.assertNotContains(
            response=response, status_code=404, text=self.test_document.label
        )

    def test_document_smart_link_list_view_with_full_access(self):
        self.grant_access(
            obj=self.test_smart_links[0],
            permission=permission_smart_link_view
        )
        self.grant_access(
            obj=self.test_smart_links[1],
            permission=permission_smart_link_view
        )
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        response = self._request_test_smart_link_document_instances_view()
        # Text must appear 5 times: 3 for the windows title and template
        # heading, plus 2 for the test.
        self.assertContains(
            count=5, response=response, status_code=200,
            text=self.test_document.label
        )

    def test_document_resolved_smart_list_with_no_permission(self):
        response = self._request_test_document_resolved_smart_link_view()
        self.assertEqual(response.status_code, 404)

    def test_document_resolved_smart_list_with_document_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        response = self._request_test_document_resolved_smart_link_view()
        self.assertEqual(response.status_code, 404)

    def test_document_resolved_smart_list_with_smart_link_access(self):
        self.grant_access(
            obj=self.test_smart_links[0],
            permission=permission_smart_link_view
        )
        self.grant_access(
            obj=self.test_smart_links[1],
            permission=permission_smart_link_view
        )

        response = self._request_test_document_resolved_smart_link_view()
        self.assertEqual(response.status_code, 404)

    def test_document_resolved_smart_list_with_full_access(self):
        self.grant_access(
            obj=self.test_smart_links[0],
            permission=permission_smart_link_view
        )
        self.grant_access(
            obj=self.test_smart_links[1],
            permission=permission_smart_link_view
        )
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        response = self._request_test_document_resolved_smart_link_view()
        self.assertEqual(response.status_code, 200)
