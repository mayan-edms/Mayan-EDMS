from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation.api import Link
from icons.api import get_icon_name, get_sprite_name
from icons.literals import APP

#from .permissions import PERMISSION_BACKUP_JOB_VIEW, PERMISSION_BACKUP_JOB_CREATE, PERMISSION_BACKUP_JOB_EDIT, PERMISSION_BACKUP_JOB_DELETE

app_registry_tool_link = Link(text=_(u'Apps'), view='app_list', icon=get_icon_name(APP))#, permissions=[PERMISSION_BACKUP_JOB_VIEW])
app_list = Link(text=_(u'app list'), view='app_list', sprite=get_sprite_name(APP))#, permissions=[PERMISSION_BACKUP_JOB_VIEW])
