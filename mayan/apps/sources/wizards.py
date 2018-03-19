from __future__ import unicode_literals

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.decorators import classonlymethod
from django.utils.encoding import force_text
from django.utils.http import urlencode
from django.utils.translation import ugettext_lazy as _

from formtools.wizard.views import SessionWizardView

from common.mixins import ViewPermissionCheckMixin
from documents.forms import DocumentTypeSelectForm
from metadata.forms import DocumentMetadataFormSet
from tags.forms import TagMultipleSelectionForm
from tags.models import Tag

from .models import InteractiveSource


class WizardStep(object):
    _registry = {}

    @classmethod
    def done(cls, wizard):
        return {}

    @classmethod
    def get(cls, name):
        return cls._registry[name]

    @classmethod
    def get_all(cls):
        return sorted(
            cls._registry.values(), key=lambda x: x.number
        )

    @classmethod
    def get_choices(cls, attribute_name):
        return sorted(
            [
                (step.name, getattr(step, attribute_name)) for step in cls.get_all()
            ]
        )

    @classmethod
    def get_form_initial(cls, wizard):
        return {}

    @classmethod
    def get_form_kwargs(cls, wizard):
        return {}

    @classmethod
    def register(cls, step):
        cls._registry[step.name] = step


class WizardStepDocumentType(WizardStep):
    form_class = DocumentTypeSelectForm
    label = _('Select document type')
    name = 'document_type_selection'
    number = 0

    @classmethod
    def condition(cls, wizard):
        return True

    @classmethod
    def done(cls, wizard):
        cleaned_data = wizard.get_cleaned_data_for_step(cls.name)
        if cleaned_data:
            return {
                'document_type_id': cleaned_data['document_type'].pk
            }

    @classmethod
    def get_form_kwargs(cls, wizard):
        return {'user': wizard.request.user}


class WizardStepMetadata(WizardStep):
    form_class = DocumentMetadataFormSet
    label = _('Enter document metadata')
    name = 'metadata_entry'
    number = 1

    @classmethod
    def condition(cls, wizard):
        """
        Skip step if document type has no associated metadata
        """
        cleaned_data = wizard.get_cleaned_data_for_step(WizardStepDocumentType.name) or {}

        document_type = cleaned_data.get('document_type')

        if document_type:
            return document_type.metadata.exists()

    @classmethod
    def get_form_initial(cls, wizard):
        initial = []

        step_data = wizard.get_cleaned_data_for_step(WizardStepDocumentType.name)
        if step_data:
            document_type = step_data['document_type']
            for document_type_metadata_type in document_type.metadata.all():
                initial.append(
                    {
                        'document_type': document_type,
                        'metadata_type': document_type_metadata_type.metadata_type,
                    }
                )

        return initial

    @classmethod
    def done(cls, wizard):
        result = {}
        cleaned_data = wizard.get_cleaned_data_for_step(cls.name)
        if cleaned_data:
            for identifier, metadata in enumerate(wizard.get_cleaned_data_for_step(cls.name)):
                if metadata.get('update'):
                    result['metadata%s_id' % identifier] = metadata['id']
                    result['metadata%s_value' % identifier] = metadata['value']

        return result


class WizardStepTags(WizardStep):
    form_class = TagMultipleSelectionForm
    label = _('Select tags')
    name = 'tag_selection'
    number = 2

    @classmethod
    def condition(cls, wizard):
        return Tag.objects.exists()

    @classmethod
    def get_form_kwargs(self, wizard):
        return {
            'help_text': _('Tags to be attached.'),
            'user': wizard.request.user
        }

    @classmethod
    def done(cls, wizard):
        result = {}
        cleaned_data = wizard.get_cleaned_data_for_step(cls.name)
        if cleaned_data:
            result['tags'] = [
                force_text(tag.pk) for tag in cleaned_data['tags']
            ]

        return result


WizardStep.register(WizardStepDocumentType)
WizardStep.register(WizardStepMetadata)
WizardStep.register(WizardStepTags)


class DocumentCreateWizard(ViewPermissionCheckMixin, SessionWizardView):
    template_name = 'appearance/generic_wizard.html'

    @classonlymethod
    def as_view(cls, *args, **kwargs):
        cls.form_list = WizardStep.get_choices(attribute_name='form_class')
        cls.condition_dict = dict(WizardStep.get_choices(attribute_name='condition'))
        return super(DocumentCreateWizard, cls).as_view(*args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not InteractiveSource.objects.filter(enabled=True).exists():
            messages.error(
                request,
                _(
                    'No interactive document sources have been defined or '
                    'none have been enabled, create one before proceeding.'
                )
            )
            return HttpResponseRedirect(reverse('sources:setup_source_list'))

        return super(
            DocumentCreateWizard, self
        ).dispatch(request, *args, **kwargs)

    def get_context_data(self, form, **kwargs):
        context = super(
            DocumentCreateWizard, self
        ).get_context_data(form=form, **kwargs)

        wizard_step = WizardStep.get(name=self.steps.current)

        context.update({
            'step_title': _(
                'Step %(step)d of %(total_steps)d: %(step_label)s'
            ) % {
                'step': self.steps.step1, 'total_steps': len(self.form_list),
                'step_label': wizard_step.label,
            },
            'submit_label': _('Next step'),
            'submit_icon': 'fa fa-arrow-right',
            'title': _('Document upload wizard'),
        })
        return context

    def get_form_initial(self, step):
        return WizardStep.get(name=step).get_form_initial(wizard=self) or {}

    def get_form_kwargs(self, step):
        return WizardStep.get(name=step).get_form_kwargs(wizard=self) or {}

    def done(self, form_list, **kwargs):
        query_dict = {}

        for step in WizardStep.get_all():
            query_dict.update(step.done(wizard=self) or {})

        url = '?'.join(
            [
                reverse('sources:upload_interactive'),
                urlencode(query_dict, doseq=True)
            ]
        )
        return HttpResponseRedirect(url)
