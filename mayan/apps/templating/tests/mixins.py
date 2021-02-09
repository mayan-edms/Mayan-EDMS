from ..classes import Template

from .literals import TEST_TEMPLATE


class DocumentTemplateSandboxViewTestMixin:
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


class TemplateTagTestMixin:
    def _render_test_template(self, template_string, context=None):
        template = Template(template_string=template_string)
        return template.render(context=context)
