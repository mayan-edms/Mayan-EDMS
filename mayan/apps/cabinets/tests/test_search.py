from unittest import skip

from mayan.apps.documents.models.document_models import Document
from mayan.apps.documents.permissions import permission_document_view
from mayan.apps.documents.search import search_model_document
from mayan.apps.documents.tests.base import GenericDocumentViewTestCase
from mayan.apps.dynamic_search.tests.mixins import SearchTestMixin

from ..models import Cabinet
from ..permissions import permission_cabinet_view
from ..search import search_model_cabinet

from .mixins import CabinetTestMixin


@skip('Slow test needs to be enabled manually.')
class CabinetSearchFieldSizeLimitTestCase(
    CabinetTestMixin, SearchTestMixin, GenericDocumentViewTestCase
):
    auto_create_test_cabinet = True
    auto_upload_test_document = False

    def _do_test_search(self):
        return self.search_backend.search(
            search_model=search_model_cabinet, query={
                'documents__uuid': str(self._test_document_stubs[0].uuid)
            }, user=self._test_case_user
        )

    def setUp(self):
        super().setUp()
        self._test_document_stubs = []
        for i in range(1000):
            self._test_document_stubs.append(
                Document(
                    document_type=self._test_document_type,
                    label='test_document_stub_{}'.format(i)
                )
            )
        Document.objects.bulk_create(self._test_document_stubs)

    def test_search_model_cabinet_with_access(self):
        self.grant_access(
            obj=self._test_cabinet, permission=permission_cabinet_view
        )

        self._clear_events()

        ThroughModel = Cabinet.documents.through

        cabinet_documents = []
        for document in Document.objects.all().only('pk'):
            cabinet_documents.append(
                ThroughModel(
                    cabinet_id=self._test_cabinet.pk, document_id=document.pk
                )
            )

        ThroughModel.objects.bulk_create(cabinet_documents)

        self.search_backend.index_instance(instance=self._test_cabinet)

        queryset = self._do_test_search()
        self.assertTrue(self._test_cabinet in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)


class CabinetSearchTestCase(
    CabinetTestMixin, SearchTestMixin, GenericDocumentViewTestCase
):
    _test_cabinet_add_test_document = True
    auto_create_test_cabinet = True

    def _do_test_search(self):
        return self.search_backend.search(
            search_model=search_model_cabinet, query={
                'documents__label': self._test_document.label
            }, user=self._test_case_user
        )

    def test_search_model_cabinet_no_permission(self):
        self._clear_events()

        queryset = self._do_test_search()
        self.assertTrue(self._test_cabinet not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_search_model_cabinet_with_access(self):
        self.grant_access(
            obj=self._test_cabinet, permission=permission_cabinet_view
        )

        self._clear_events()

        queryset = self._do_test_search()
        self.assertTrue(self._test_cabinet in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_search_model_document_model_cabinet_with_access(self):
        self.grant_access(
            obj=self._test_cabinet, permission=permission_cabinet_view
        )

        self._test_document.delete()

        self._clear_events()

        queryset = self._do_test_search()
        self.assertTrue(self._test_cabinet in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)


class DocumentCabinetSearchTestCase(
    CabinetTestMixin, SearchTestMixin, GenericDocumentViewTestCase
):
    _test_cabinet_add_test_document = True
    auto_create_test_cabinet = True

    def _do_test_search(self):
        return self.search_backend.search(
            search_model=search_model_document, query={
                'cabinets__label': self._test_cabinet.label
            }, user=self._test_case_user
        )

    def test_search_model_document_no_permission(self):
        self._clear_events()

        queryset = self._do_test_search()
        self.assertTrue(self._test_document not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_search_model_document_with_access(self):
        self.grant_access(
            obj=self._test_document, permission=permission_document_view
        )

        self._clear_events()

        queryset = self._do_test_search()
        self.assertTrue(self._test_document in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_search_model_document_with_access(self):
        self.grant_access(
            obj=self._test_document, permission=permission_document_view
        )

        self._test_document.delete()

        self._clear_events()

        queryset = self._do_test_search()
        self.assertTrue(self._test_document not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
