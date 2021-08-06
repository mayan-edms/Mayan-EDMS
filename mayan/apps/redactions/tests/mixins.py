from ..layers import layer_redactions


class LayerMaximumOrderAPIViewTestMixin:
    def _request_document_file_page_image_api_view_with_maximum_layer_order(self):
        return self.get(
            viewname='rest_api:documentfilepage-image', kwargs={
                'document_id': self.test_document.pk,
                'document_file_id': self.test_document_file.pk,
                'document_file_page_id': self.test_document_file_page.pk,
            }, query={'maximum_layer_order': layer_redactions.order}
        )
