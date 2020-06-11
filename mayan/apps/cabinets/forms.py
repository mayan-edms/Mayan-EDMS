import logging

from django.utils.translation import ugettext_lazy as _

from mayan.apps.views.forms import FilteredSelectionForm

logger = logging.getLogger(name=__name__)


class CabinetListForm(FilteredSelectionForm):
    class Meta:
        allow_multiple = True
        field_name = 'cabinets'
        label = _('Cabinets')
        required = False
        widget_attributes = {'class': 'select2'}
