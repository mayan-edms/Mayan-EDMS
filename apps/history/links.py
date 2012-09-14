from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation import Link

from .permissions import PERMISSION_HISTORY_VIEW
from .icons import icon_history_list, icon_history_details

history_list = Link(text=_(u'history'), view='history_list', icon=icon_history_list, permissions=[PERMISSION_HISTORY_VIEW], children_view_regex=[r'history_[l,v]'])
history_details = Link(text=_(u'details'), view='history_view', icon=icon_history_details, args='object.pk', permissions=[PERMISSION_HISTORY_VIEW])
