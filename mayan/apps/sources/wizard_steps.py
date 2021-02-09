from django.utils.translation import ugettext_lazy as _

from mayan.apps.documents.forms.document_type_forms import DocumentTypeFilteredSelectForm
from mayan.apps.documents.permissions import permission_document_create

from .classes import DocumentCreateWizardStep


class DocumentCreateWizardStepDocumentType(DocumentCreateWizardStep):
    form_class = DocumentTypeFilteredSelectForm
    label = _('Select document type')
    name = 'document_type_selection'
    number = 0

    @classmethod
    def condition(cls, wizard):
        return True

    @classmethod
    def done(cls, wizard):
        cleaned_data = wizard.get_cleaned_data_for_step(step=cls.name)
        if cleaned_data:
            return {
                'document_type_id': cleaned_data['document_type'].pk
            }

    @classmethod
    def get_form_kwargs(cls, wizard):
        return {
            'permission': permission_document_create,
            'user': wizard.request.user
        }


DocumentCreateWizardStep.register(DocumentCreateWizardStepDocumentType)
