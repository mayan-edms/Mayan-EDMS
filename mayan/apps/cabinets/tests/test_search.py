from mayan.apps.documents.tests.base import GenericDocumentViewTestCase

from ..permissions import permission_cabinet_view

from .mixins import CabinetSearchTestMixin, CabinetTestMixin


class CabinetSearchTestCase(
    CabinetTestMixin, CabinetSearchTestMixin, GenericDocumentViewTestCase
):
    def setUp(self):
        super().setUp()
        self._create_test_cabinet(add_test_document=True)

    def test_cabinet_search_no_permission(self):
        queryset = self._perform_cabinet_search()
        self.assertFalse(self.test_cabinet in queryset)

    def test_cabinet_search_with_access(self):
        self.grant_access(
            obj=self.test_cabinet, permission=permission_cabinet_view
        )

        queryset = self._perform_cabinet_search()
        self.assertTrue(self.test_cabinet in queryset)
