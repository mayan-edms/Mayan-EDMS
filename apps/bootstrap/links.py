from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation import Link

from .permissions import PERMISSION_BOOTSTRAP_EXECUTE, PERMISSION_NUKE_DATABASE
from .icons import icon_database_bootstrap, icon_bootstrap_execute, icon_nuke_database

database_bootstrap = Link(text=_(u'bootstrap database'), view='bootstrap_type_list', icon=icon_database_bootstrap, permissions=[PERMISSION_BOOTSTRAP_EXECUTE])
bootstrap_execute = Link(text=_(u'execute'), view='bootstrap_execute', args='object.pk', icon=icon_bootstrap_execute, permissions=[PERMISSION_BOOTSTRAP_EXECUTE])
link_erase_database = Link(text=_(u'erase database'), view='erase_database_view', icon=icon_nuke_database, permissions=[PERMISSION_NUKE_DATABASE])
