from ..permissions import permission_document_view
from ..widgets import DocumentPageThumbnailWidget

from .base import GenericDocumentTestCase, GenericDocumentViewTestCase
from .mixins import DocumentViewTestMixin


class DocumentPageWidgetTestCase(GenericDocumentTestCase):
    def test_document_list_view_document_with_no_pages(self):
        document_thumbnail_widget = DocumentPageThumbnailWidget()
        self.test_document.pages.all().delete()
        result = document_thumbnail_widget.render(instance=self.test_document)

        self.assertTrue(self.test_document.get_absolute_url() in result)


class DocumentPreviewWidgetViewTestCase(
    DocumentViewTestMixin, GenericDocumentViewTestCase
):
    def test_document_preview_page_carousel_widget_render(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        response = self._request_test_document_preview_view()
        self.assertContains(
            response=response, status_code=200, text='carousel-container'
        )
