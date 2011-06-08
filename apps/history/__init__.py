from django.utils.translation import ugettext_lazy as _

from navigation.api import register_links
from permissions.api import register_permission, set_namespace_title

PERMISSION_HISTORY_VIEW = {'namespace': 'history', 'name': u'history_view', 'label': _(u'Access the history app')}

set_namespace_title('history', _(u'history'))
register_permission(PERMISSION_HISTORY_VIEW)

# TODO: support permissions AND operand
history_list = {'text': _(u'history'), 'view': 'history_list', 'famfam': 'book', 'permissions': [PERMISSION_HISTORY_VIEW]}

#register_links(['history_view'], [history_list], menu_name='sidebar')
