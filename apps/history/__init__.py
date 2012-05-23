from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from project_tools.api import register_tool
from navigation.api import Link

from .permissions import PERMISSION_HISTORY_VIEW

register_tool(Link(text=_(u'history'), view='history_list', sprite='book', icon='book.png', permissions=[PERMISSION_HISTORY_VIEW], children_view_regex=[r'history_[l,v]']))
