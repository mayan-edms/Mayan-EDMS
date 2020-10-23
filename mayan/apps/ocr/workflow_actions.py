from django.utils.translation import ugettext_lazy as _

from mayan.apps.document_states.classes import WorkflowAction
from mayan.apps.documents.models.document_page_models import DocumentPage
from mayan.apps.templating.classes import Template

from .models import DocumentPageOCRContent

__all__ = ('UpdateDocumentPageOCRAction',)


class UpdateDocumentPageOCRAction(WorkflowAction):
    fields = {
        'page_condition': {
            'label': _('Page condition'),
            'class': 'mayan.apps.templating.fields.ModelTemplateField',
            'kwargs': {
                'initial_help_text': _(
                    'The condition that will determine if a document page\'s '
                    'OCR content will be modified or not. The condition is '
                    'evaluated against the iterated document page. '
                    'Conditions that do not return any value, that return '
                    'the Python logical None, or an empty string (\'\') '
                    'are considered to be logical false, any other value is '
                    'considered to be the logical true.'
                ), 'required': False, 'model': DocumentPage,
                'model_variable': 'document_page',
            }
        },
        'page_content': {
            'label': _('Page content'),
            'class': 'mayan.apps.templating.fields.ModelTemplateField',
            'kwargs': {
                'initial_help_text': _(
                    'A template that will generate the OCR content to be '
                    'saved.'
                ), 'required': False, 'model': DocumentPage,
                'model_variable': 'document_page',
            }
        },
    }
    field_order = ('page_condition', 'page_content')
    label = _('Update document page OCR content')

    def evaluate_condition(self, context, condition=None):
        if condition:
            return Template(template_string=condition).render(
                context=context
            ).strip()
        else:
            return False

    def execute(self, context):
        for document_page in context['document'].pages_valid:
            context['document_page'] = document_page
            if self.evaluate_condition(context=context, condition=self.form_data['page_condition']):
                DocumentPageOCRContent.objects.update_or_create(
                    document_page=document_page, defaults={
                        'content': Template(
                            template_string=self.form_data['page_content']
                        ).render(context=context)
                    }
                )
