from django.test import RequestFactory

from ..dashboard_widgets import DashboardWidgetUserRecentlyCreatedDocuments
from ..permissions import permission_document_view

from .base import GenericDocumentViewTestCase


class DashboardWidgetUserRecentlyCreatedDocumentsTestCase(
    GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_document_stub()

    def test_widget_no_permission(self):
        widget = DashboardWidgetUserRecentlyCreatedDocuments()

        request = RequestFactory()
        request.user = self._test_case_user
        widget.request = request

        self.assertTrue(self._test_document not in widget.get_object_list())

    def test_widget_with_access(self):
        self.grant_access(
            obj=self._test_document, permission=permission_document_view
        )

        widget = DashboardWidgetUserRecentlyCreatedDocuments()

        request = RequestFactory()
        request.user = self._test_case_user
        widget.request = request

        self.assertTrue(self._test_document in widget.get_object_list())
