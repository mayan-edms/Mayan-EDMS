from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation.api import Link

from .permissions import PERMISSION_BOOTSTRAP_EXECUTE, PERMISSION_NUKE_DATABASE

database_bootstrap = Link(text=_(u'bootstrap database'), view='bootstrap_type_list', icon='database_lightning.png', permissions=[PERMISSION_BOOTSTRAP_EXECUTE])
bootstrap_execute = Link(text=_(u'execute'), view='bootstrap_execute', args='object.name', sprite='database_lightning', permissions=[PERMISSION_BOOTSTRAP_EXECUTE])
erase_database_link = Link(text=_(u'erase database'), view='erase_database_view', icon='radioactivity.png', permissions=[PERMISSION_NUKE_DATABASE])
