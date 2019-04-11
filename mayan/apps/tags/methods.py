from __future__ import unicode_literals

from django.apps import apps
from django.utils.translation import ugettext_lazy as _


def method_document_get_tags(self):
    DocumentTag = apps.get_model(app_label='tags', model_name='DocumentTag')

    return DocumentTag.objects.filter(documents=self)


method_document_get_tags.help_text = _(
    'Return a the tags attached to the document.'
)
