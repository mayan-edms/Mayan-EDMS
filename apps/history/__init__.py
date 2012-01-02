from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from project_tools.api import register_tool

from .permissions import PERMISSION_HISTORY_VIEW

# TODO: support permissions AND operand
# encapsulate into document_history_list and require DOCUMENT_VIEW and HISTORY_VIEW
history_list = {'text': _(u'history'), 'view': 'history_list', 'famfam': 'book', 'icon': 'book.png', 'permissions': [PERMISSION_HISTORY_VIEW], 'children_views': ['history_view']}

register_tool(history_list)
