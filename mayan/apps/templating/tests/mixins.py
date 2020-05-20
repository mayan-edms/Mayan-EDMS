from .literals import TEST_TEMPLATE


class DocumentTemplateSandboxViewTestMixin(object):
    def _request_document_template_sandbox_get_view(self):
        return self.get(
            viewname='templating:document_template_sandbox', kwargs={
                'document_id': self.test_document.pk
            }
        )

    def _request_document_template_sandbox_post_view(self):
        return self.post(
            viewname='templating:document_template_sandbox', kwargs={
                'document_id': self.test_document.pk
            }, data={'template_template': TEST_TEMPLATE}
        )
