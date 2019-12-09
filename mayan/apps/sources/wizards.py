from __future__ import unicode_literals

from furl import furl

from django.apps import apps
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.decorators import classonlymethod
from django.utils.translation import ugettext_lazy as _

from formtools.wizard.views import SessionWizardView

from mayan.apps.documents.forms import DocumentTypeFilteredSelectForm
from mayan.apps.documents.permissions import permission_document_create

from .icons import icon_wizard_submit


class WizardStep(object):
    _deregistry = {}
    _registry = {}

    @classmethod
    def deregister(cls, step):
        cls._deregistry[step.name] = step

    @classmethod
    def deregister_all(cls):
        for step in cls.get_all():
            cls.deregister(step=step)

    @classmethod
    def done(cls, wizard):
        return {}

    @classmethod
    def get(cls, name):
        for step in cls.get_all():
            if name == step.name:
                return step

    @classmethod
    def get_all(cls):
        return sorted(
            [
                step for step in cls._registry.values() if step.name not in cls._deregistry
            ], key=lambda x: x.number
        )

    @classmethod
    def get_choices(cls, attribute_name):
        return [
            (step.name, getattr(step, attribute_name)) for step in cls.get_all()
        ]

    @classmethod
    def get_form_initial(cls, wizard):
        return {}

    @classmethod
    def get_form_kwargs(cls, wizard):
        return {}

    @classmethod
    def post_upload_process(cls, document, querystring=None):
        for step in cls.get_all():
            step.step_post_upload_process(
                document=document, querystring=querystring
            )

    @classmethod
    def register(cls, step):
        if step.name in cls._registry:
            raise Exception('A step with this name already exists: %s' % step.name)

        if step.number in [reigstered_step.number for reigstered_step in cls.get_all()]:
            raise Exception('A step with this number already exists: %s' % step.name)

        cls._registry[step.name] = step

    @classmethod
    def reregister(cls, name):
        cls._deregistry.pop(name)

    @classmethod
    def reregister_all(cls):
        cls._deregistry = {}

    @classmethod
    def step_post_upload_process(cls, document, querystring=None):
        pass


class WizardStepDocumentType(WizardStep):
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


WizardStep.register(WizardStepDocumentType)


class DocumentCreateWizard(SessionWizardView):
    template_name = 'appearance/generic_wizard.html'

    @classonlymethod
    def as_view(cls, *args, **kwargs):
        cls.form_list = WizardStep.get_choices(attribute_name='form_class')
        cls.condition_dict = dict(
            WizardStep.get_choices(attribute_name='condition')
        )
        return super(DocumentCreateWizard, cls).as_view(*args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        InteractiveSource = apps.get_model(
            app_label='sources', model_name='InteractiveSource'
        )

        form_list = WizardStep.get_choices(attribute_name='form_class')
        condition_dict = dict(
            WizardStep.get_choices(attribute_name='condition')
        )

        result = self.__class__.get_initkwargs(
            condition_dict=condition_dict, form_list=form_list
        )
        self.form_list = result['form_list']
        self.condition_dict = result['condition_dict']

        if not InteractiveSource.objects.filter(enabled=True).exists():
            messages.error(
                message=_(
                    'No interactive document sources have been defined or '
                    'none have been enabled, create one before proceeding.'
                ),
                request=request
            )
            return HttpResponseRedirect(
                redirect_to=reverse(viewname='sources:setup_source_list')
            )

        return super(
            DocumentCreateWizard, self
        ).dispatch(request, *args, **kwargs)

    def get_context_data(self, form, **kwargs):
        context = super(
            DocumentCreateWizard, self
        ).get_context_data(form=form, **kwargs)

        wizard_step = WizardStep.get(name=self.steps.current)

        context.update(
            {
                'form_css_classes': 'form-hotkey-double-click',
                'step_title': _(
                    'Step %(step)d of %(total_steps)d: %(step_label)s'
                ) % {
                    'step': self.steps.step1, 'total_steps': len(self.form_list),
                    'step_label': wizard_step.label,
                },
                'submit_label': _('Next step'),
                'submit_icon_class': icon_wizard_submit,
                'title': _('Document upload wizard'),
                'wizard_step': wizard_step,
                'wizard_steps': WizardStep.get_all(),
            }
        )
        return context

    def get_form_initial(self, step):
        return WizardStep.get(name=step).get_form_initial(wizard=self) or {}

    def get_form_kwargs(self, step):
        return WizardStep.get(name=step).get_form_kwargs(wizard=self) or {}

    def done(self, form_list, **kwargs):
        query_dict = {}

        for step in WizardStep.get_all():
            query_dict.update(step.done(wizard=self) or {})

        url = furl(reverse(viewname='sources:document_upload_interactive'))
        # Use equal and not .update() to get the same result as using
        # urlencode(doseq=True)
        url.args = query_dict

        return HttpResponseRedirect(redirect_to=url)
