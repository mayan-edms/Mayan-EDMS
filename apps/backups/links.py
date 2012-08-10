from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation.api import Link

#from .permissions import 

backup_tool_link = Link(text=_(u'backup'), view='backup_view', icon='cd_burn.png')#, permissions=[])
restore_tool_link = Link(text=_(u'restore'), view='restore_view', icon='cd_eject.png')#, permissions=[])
