from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation.api import Link

from .permissions import PERMISSION_HISTORY_VIEW

history_list = Link(text=_(u'history'), view='history_list', sprite='book', icon='book.png', permissions=[PERMISSION_HISTORY_VIEW], children_view_regex=[r'history_[l,v]'])
history_details = Link(text=_(u'details'), view='history_view', sprite='book_open', args='object.pk', permissions=[PERMISSION_HISTORY_VIEW])
