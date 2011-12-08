from django.utils.translation import ugettext_lazy as _

from project_tools.api import register_tool
from permissions.models import PermissionNamespace, Permission

history_namespace = PermissionNamespace('history', _(u'History'))

PERMISSION_HISTORY_VIEW = Permission.objects.register(history_namespace, 'history_view', _(u'Access the history app'))

# TODO: support permissions AND operand
# encapsulate into document_history_list and require DOCUMENT_VIEW and HISTORY_VIEW
history_list = {'text': _(u'history'), 'view': 'history_list', 'famfam': 'book', 'icon': 'book.png', 'permissions': [PERMISSION_HISTORY_VIEW], 'children_views': ['history_view']}

register_tool(history_list)
