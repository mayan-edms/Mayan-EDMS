from __future__ import unicode_literals

from furl import furl

from django.apps import apps
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _

from sources.wizards import WizardStep

from .forms import TagMultipleSelectionForm


class WizardStepTags(WizardStep):
    form_class = TagMultipleSelectionForm
    label = _('Select tags')
    name = 'tag_selection'
    number = 2

    @classmethod
    def condition(cls, wizard):
        Tag = apps.get_model(app_label='tags', model_name='Tag')
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

    @classmethod
    def step_post_upload_process(cls, document, querystring=None):
        furl_instance = furl(querystring)
        Tag = apps.get_model(app_label='tags', model_name='Tag')

        tag_id_list = furl_instance.args.get('tags', '')

        if tag_id_list:
            tag_id_list = tag_id_list.split(',')

        for tag in Tag.objects.filter(pk__in=tag_id_list):
            tag.documents.add(document)


WizardStep.register(WizardStepTags)
