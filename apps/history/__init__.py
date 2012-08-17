from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from backups.api import AppBackup, ModelBackup
from app_registry import register_app, UnableToRegister
from common.utils import encapsulate
from navigation.api import bind_links, register_model_list_columns
from project_tools.api import register_tool

from .models import History
from .widgets import history_entry_type_link
from .links import history_list, history_details

register_tool(history_list)

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

try:
    app = register_app('history', _(u'History'))
except UnableToRegister:
    pass
else:
    AppBackup(app, [ModelBackup()])
