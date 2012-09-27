from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from common.utils import encapsulate
from navigation.api import bind_links, register_model_list_columns

from .models import History
from .widgets import history_entry_type_link
from history.links import history_details

register_model_list_columns(History, [
    {
        'name': _(u'date and time'),
        'attribute': 'datetime'
    },
    {
        'name': _(u'type'),
        'attribute': encapsulate(lambda entry: history_entry_type_link(entry))
    },
    {
        'name': _(u'summary'),
        'attribute': encapsulate(lambda entry: unicode(entry.get_processed_summary()))
    }
])

bind_links([History], [history_details])
