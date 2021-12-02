from furl import furl

from django import forms
from django.apps import apps
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.decorators import classonlymethod
from django.utils.translation import ugettext_lazy as _

from formtools.wizard.views import SessionWizardView

from .classes import DocumentCreateWizardStep
from .icons import (
    icon_wizard_step_first, icon_wizard_step_next, icon_wizard_step_previous
)


class DocumentCreateWizard(SessionWizardView):
    template_name = 'appearance/generic_wizard.html'

    @classonlymethod
    def as_view(cls, *args, **kwargs):
        # SessionWizardView needs at least one form in order to be
        # initialized as a view. Declare one empty form and then change the
        # form list in the .dispatch() method.
        class EmptyForm(forms.Form):
            """Empty form"""

        cls.form_list = [EmptyForm]
        return super().as_view(*args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        Source = apps.get_model(
            app_label='sources', model_name='Source'
        )

        form_list = DocumentCreateWizardStep.get_choices(attribute_name='form_class')
        condition_dict = dict(
            DocumentCreateWizardStep.get_choices(attribute_name='condition')
        )

        result = self.__class__.get_initkwargs(
            condition_dict=condition_dict, form_list=form_list
        )
        self.form_list = result['form_list']
        self.condition_dict = result['condition_dict']

        if not Source.objects.interactive().filter(enabled=True).exists():
            messages.error(
                message=_(
                    'No interactive document sources have been defined or '
                    'none have been enabled, create one before proceeding.'
                ), request=request
            )
            return HttpResponseRedirect(
                redirect_to=reverse(viewname='sources:source_list')
            )

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)

        wizard_step = DocumentCreateWizardStep.get(name=self.steps.current)

        context.update(
            {
                'form_css_classes': 'form-hotkey-enter form-hotkey-double-click',
                'step_title': _(
                    'Step %(step)d of %(total_steps)d: %(step_label)s'
                ) % {
                    'step': self.steps.step1, 'total_steps': len(self.form_list),
                    'step_label': wizard_step.label,
                },
                'title': _('Document upload wizard'),
                'wizard_step': wizard_step,
                'wizard_steps': DocumentCreateWizardStep.get_all(),
            }
        )

        context['form_button_overrides'] = (
            {
                'icon': icon_wizard_step_first,
                'label': _('First'),
                'name_override': 'wizard_goto_step',
                'value': self.steps.first
            },
            {
                'icon': icon_wizard_step_previous,
                'label': _('Previous'),
                'name_override': 'wizard_goto_step',
                'value': self.steps.prev
            },
            {
                'icon': icon_wizard_step_next,
                'is_primary': True,
                'label': _('Next')
            }
        )

        if not self.steps.prev:
            context['form_button_overrides'][0]['css_classes'] = 'disabled'
            context['form_button_overrides'][0]['disabled'] = True
            context['form_button_overrides'][1]['css_classes'] = 'disabled'
            context['form_button_overrides'][1]['disabled'] = True

        return context

    def get_form_initial(self, step):
        return DocumentCreateWizardStep.get(name=step).get_form_initial(wizard=self) or {}

    def get_form_kwargs(self, step):
        return DocumentCreateWizardStep.get(name=step).get_form_kwargs(wizard=self) or {}

    def done(self, form_list, **kwargs):
        query_dict = {}

        for step in DocumentCreateWizardStep.get_all():
            query_dict.update(step.done(wizard=self) or {})

        url = furl(reverse(viewname='sources:document_upload_interactive'))
        # Use equal and not .update() to get the same result as using
        # urlencode(doseq=True)
        url.args = query_dict

        return HttpResponseRedirect(redirect_to=url.tostr())
