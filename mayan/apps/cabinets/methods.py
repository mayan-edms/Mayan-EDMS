from __future__ import unicode_literals

from django.apps import apps
from django.utils.translation import ugettext_lazy as _


def method_get_document_cabinets(self):
    DocumentCabinet = apps.get_model(
        app_label='cabinets', model_name='DocumentCabinet'
    )

    return DocumentCabinet.objects.filter(documents=self).order_by(
        'parent__label', 'label'
    )


method_get_document_cabinets.help_text = _(
    'Return a list of cabinets containing the document'
)
method_get_document_cabinets.short_description = _('get_cabinets()')
