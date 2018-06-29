from __future__ import unicode_literals

from furl import furl

from django.apps import apps
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _

from sources.wizards import WizardStep

from .forms import CabinetListForm


class WizardStepCabinets(WizardStep):
    form_class = CabinetListForm
    label = _('Select cabinets')
    name = 'cabinet_selection'
    number = 3

    @classmethod
    def condition(cls, wizard):
        Cabinet = apps.get_model(
            app_label='cabinets', model_name='Cabinet'
        )
        return Cabinet.objects.exists()

    @classmethod
    def get_form_kwargs(self, wizard):
        return {
            'help_text': _('Cabinets to which the document will be added.'),
            'user': wizard.request.user
        }

    @classmethod
    def done(cls, wizard):
        result = {}
        cleaned_data = wizard.get_cleaned_data_for_step(cls.name)
        if cleaned_data:
            result['cabinets'] = [
                force_text(cabinet.pk) for cabinet in cleaned_data['cabinets']
            ]

        return result

    @classmethod
    def step_post_upload_process(cls, document, querystring=None):
        furl_instance = furl(querystring)
        Cabinet = apps.get_model(app_label='cabinets', model_name='Cabinet')

        for cabinet in Cabinet.objects.filter(pk__in=furl_instance.args.getlist('cabinets')):
            cabinet.documents.add(document)


WizardStep.register(WizardStepCabinets)
