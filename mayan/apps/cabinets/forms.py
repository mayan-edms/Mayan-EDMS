from __future__ import absolute_import, unicode_literals

import logging

from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.forms import FilteredSelectionForm

logger = logging.getLogger(__name__)


class CabinetListForm(FilteredSelectionForm):
    class Meta:
        allow_multiple = True
        field_name = 'cabinets'
        label = _('Cabinets')
        required = False
        widget_attributes = {'class': 'select2'}
