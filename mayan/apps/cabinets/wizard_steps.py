from django.apps import apps
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _

from mayan.apps.sources.wizards import WizardStep
from mayan.apps.views.http import URL

from .forms import CabinetListForm
from .models import Cabinet
from .permissions import permission_cabinet_add_document


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
            'permission': permission_cabinet_add_document,
            'queryset': Cabinet.objects.all(),
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
        Cabinet = apps.get_model(app_label='cabinets', model_name='Cabinet')
        cabinet_id_list = URL(query_string=querystring).args.getlist('cabinets')

        for cabinet in Cabinet.objects.filter(pk__in=cabinet_id_list):
            cabinet.documents.add(document)


WizardStep.register(WizardStepCabinets)
