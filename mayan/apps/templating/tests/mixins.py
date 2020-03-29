class DocumentTemplateSandboxViewTestMixin(object):
    def _request_document_template_sandbox_view(self):
        return self.get(
            viewname='templating:document_template_sandbox', kwargs={
                'document_id': self.test_document.pk
            }
        )
