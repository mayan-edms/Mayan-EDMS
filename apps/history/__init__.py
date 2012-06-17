from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from project_tools.api import register_tool

from .permissions import PERMISSION_HISTORY_VIEW

history_list = {'text': _(u'history'), 'view': 'history_list', 'famfam': 'book', 'icon': 'book.png', 'children_view_regex': [r'history_[l,v]']}

register_tool(history_list)
