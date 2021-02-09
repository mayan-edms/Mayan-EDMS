from django.utils.encoding import force_text

from mayan.apps.documents.permissions import (
    permission_document_file_view, permission_document_version_view,
    permission_document_view
)
from mayan.apps.documents.search import (
    document_file_page_search, document_file_search, document_search,
    document_version_page_search, document_version_search
)
from mayan.apps.documents.tests.base import GenericDocumentViewTestCase
from mayan.apps.documents.tests.mixins.document_mixins import DocumentViewTestMixin
from mayan.apps.dynamic_search.tests.mixins import SearchViewTestMixin

from ..permissions import permission_tag_view

from .mixins import TagTestMixin


class DocumentTagHTMLWidgetTestCase(
    DocumentViewTestMixin, TagTestMixin, GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_document_stub()

    def test_document_tags_widget_no_permission(self):
        self._create_test_tag(add_test_document=True)

        response = self._request_test_document_list_view()
        self.assertNotContains(
            response=response, text=self.test_document.label, status_code=200
        )
        self.assertNotContains(
            response=response, text=self.test_tag.label, status_code=200
        )

    def test_document_tags_widget_with_document_view_access(self):
        self._create_test_tag(add_test_document=True)

        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        response = self._request_test_document_list_view()
        self.assertContains(
            response=response, text=self.test_document.label, status_code=200
        )
        self.assertNotContains(
            response=response, text=force_text(s=self.test_tag), status_code=200
        )

    def test_document_tags_widget_with_document_tag_view_access(self):
        self._create_test_tag(add_test_document=True)

        self.grant_access(
            obj=self.test_document, permission=permission_tag_view
        )

        response = self._request_test_document_list_view()
        self.assertNotContains(
            response=response, text=self.test_document.label, status_code=200
        )
        self.assertNotContains(
            response=response, text=force_text(s=self.test_tag), status_code=200
        )

    def test_document_tags_widget_with_document_full_access(self):
        self._create_test_tag(add_test_document=True)

        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )
        self.grant_access(
            obj=self.test_document, permission=permission_tag_view
        )

        response = self._request_test_document_list_view()
        self.assertContains(
            response=response, text=self.test_document.label, status_code=200
        )
        self.assertNotContains(
            response=response, text=force_text(s=self.test_tag), status_code=200
        )

    def test_document_tags_widget_with_document_view_and_tag_view_access(self):
        self._create_test_tag(add_test_document=True)

        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )
        self.grant_access(
            obj=self.test_tag, permission=permission_tag_view
        )

        response = self._request_test_document_list_view()
        self.assertContains(
            response=response, text=self.test_document.label, status_code=200
        )
        self.assertNotContains(
            response=response, text=force_text(s=self.test_tag), status_code=200
        )

    def test_document_tags_widget_with_tag_access(self):
        self._create_test_tag(add_test_document=True)

        self.grant_access(
            obj=self.test_tag, permission=permission_tag_view
        )

        response = self._request_test_document_list_view()
        self.assertNotContains(
            response=response, text=self.test_document.label, status_code=200
        )
        self.assertNotContains(
            response=response, text=self.test_tag.label, status_code=200
        )

    def test_document_tags_widget_with_full_access(self):
        self._create_test_tag(add_test_document=True)

        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )
        self.grant_access(
            obj=self.test_document, permission=permission_tag_view
        )
        self.grant_access(
            obj=self.test_tag, permission=permission_tag_view
        )

        response = self._request_test_document_list_view()
        self.assertContains(
            response=response, text=self.test_document.label, status_code=200
        )
        self.assertContains(
            response=response, text=self.test_tag.label, status_code=200
        )


class DocumentSearchResultWidgetViewTestCase(
    DocumentViewTestMixin, SearchViewTestMixin, TagTestMixin,
    GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._upload_test_document()
        self._create_test_tag(add_test_document=True)
        self._test_object_permission = permission_document_view
        self._test_object_text = self.test_document.label
        self._test_search_model = document_search
        self._test_search_term_data = {'uuid': self.test_document.uuid}

    def test_document_tag_widget_no_permission(self):
        response = self._request_search_results_view(
            data=self._test_search_term_data, kwargs={
                'search_model_name': self._test_search_model.get_full_name()
            }
        )
        self.assertNotContains(
            response=response, text=self._test_object_text, status_code=200
        )
        self.assertNotContains(
            response=response, text=self.test_tag.label, status_code=200
        )

    def test_document_tag_widget_with_tag_type_access(self):
        self.grant_access(
            obj=self.test_tag, permission=permission_tag_view
        )

        response = self._request_search_results_view(
            data=self._test_search_term_data, kwargs={
                'search_model_name': self._test_search_model.get_full_name()
            }
        )
        self.assertNotContains(
            response=response, text=self._test_object_text, status_code=200
        )
        self.assertNotContains(
            response=response, text=self.test_tag.label, status_code=200
        )

    def test_document_tag_widget_with_document_view_access(self):
        self.grant_access(
            obj=self.test_document, permission=self._test_object_permission
        )

        response = self._request_search_results_view(
            data=self._test_search_term_data, kwargs={
                'search_model_name': self._test_search_model.get_full_name()
            }
        )
        self.assertContains(
            response=response, text=self._test_object_text, status_code=200
        )
        self.assertNotContains(
            response=response, text=self.test_tag.label, status_code=200
        )

    def test_document_tag_widget_with_document_tag_view_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_tag_view
        )

        response = self._request_search_results_view(
            data=self._test_search_term_data, kwargs={
                'search_model_name': self._test_search_model.get_full_name()
            }
        )
        self.assertNotContains(
            response=response, text=self._test_object_text, status_code=200
        )
        self.assertNotContains(
            response=response, text=self.test_tag.label, status_code=200
        )

    def test_document_tag_widget_with_all_document_access(self):
        self.grant_access(
            obj=self.test_document, permission=self._test_object_permission
        )
        self.grant_access(
            obj=self.test_document, permission=permission_tag_view
        )

        response = self._request_search_results_view(
            data=self._test_search_term_data, kwargs={
                'search_model_name': self._test_search_model.get_full_name()
            }
        )
        self.assertContains(
            response=response, text=self._test_object_text, status_code=200
        )
        self.assertNotContains(
            response=response, text=self.test_tag.label, status_code=200
        )

    def test_document_tag_widget_with_tag_view_and_document_view_access(self):
        self.grant_access(
            obj=self.test_document, permission=self._test_object_permission
        )
        self.grant_access(
            obj=self.test_tag, permission=permission_tag_view
        )

        response = self._request_search_results_view(
            data=self._test_search_term_data, kwargs={
                'search_model_name': self._test_search_model.get_full_name()
            }
        )
        self.assertContains(
            response=response, text=self._test_object_text, status_code=200
        )
        self.assertNotContains(
            response=response, text=self.test_tag.label,
            status_code=200
        )

    def test_document_tag_widget_with_full_access(self):
        self.grant_access(
            obj=self.test_document, permission=self._test_object_permission
        )
        self.grant_access(
            obj=self.test_document, permission=permission_tag_view
        )
        self.grant_access(
            obj=self.test_tag, permission=permission_tag_view
        )

        response = self._request_search_results_view(
            data=self._test_search_term_data, kwargs={
                'search_model_name': self._test_search_model.get_full_name()
            }
        )
        self.assertContains(
            response=response, text=self._test_object_text, status_code=200
        )
        self.assertContains(
            response=response, text=self.test_tag.label, status_code=200
        )


class DocumentFileSearchResultWidgetViewTestCase(
    DocumentSearchResultWidgetViewTestCase
):
    def setUp(self):
        super().setUp()
        self._test_object_text = self.test_document_file.filename
        self._test_object_permission = permission_document_file_view
        self._test_search_model = document_file_search
        self._test_search_term_data = {
            'document__uuid': self.test_document.uuid
        }


class DocumentFilePageSearchResultWidgetViewTestCase(
    DocumentSearchResultWidgetViewTestCase
):
    def setUp(self):
        super().setUp()
        self._test_object_text = force_text(s=self.test_document_file.pages.first())
        self._test_object_permission = permission_document_file_view
        self._test_search_model = document_file_page_search
        self._test_search_term_data = {
            'document_file__document__uuid': self.test_document.uuid
        }


class DocumentVersionSearchResultWidgetViewTestCase(
    DocumentSearchResultWidgetViewTestCase
):
    def setUp(self):
        super().setUp()
        self._test_object_text = force_text(s=self.test_document_version)
        self._test_object_permission = permission_document_version_view
        self._test_search_model = document_version_search
        self._test_search_term_data = {
            'document__uuid': self.test_document.uuid
        }


class DocumentVersionPageSearchResultWidgetViewTestCase(
    DocumentSearchResultWidgetViewTestCase
):
    def setUp(self):
        super().setUp()
        self._test_object_text = force_text(s=self.test_document_version.pages.first())
        self._test_object_permission = permission_document_version_view
        self._test_search_model = document_version_page_search
        self._test_search_term_data = {
            'document_version__document__uuid': self.test_document.uuid
        }
