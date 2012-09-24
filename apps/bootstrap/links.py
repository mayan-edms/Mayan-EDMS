from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation import Link

from .permissions import (PERMISSION_BOOTSTRAP_VIEW, PERMISSION_BOOTSTRAP_CREATE,
    PERMISSION_BOOTSTRAP_EDIT, PERMISSION_BOOTSTRAP_DELETE,
    PERMISSION_BOOTSTRAP_EXECUTE, PERMISSION_BOOTSTRAP_DUMP,
    PERMISSION_NUKE_DATABASE)
from .icons import (icon_bootstrap_setup, icon_bootstrap_setup_execute, icon_bootstrap_setup_create,
    icon_bootstrap_setup_edit, icon_bootstrap_setup_delete, icon_bootstrap_setup_view,
    icon_bootstrap_setup_dump, icon_nuke_database)

link_bootstrap_setup_tool = Link(text=_(u'bootstrap'), view='bootstrap_setup_list', icon=icon_bootstrap_setup, permissions=[PERMISSION_BOOTSTRAP_VIEW])
link_bootstrap_setup_list = Link(text=_(u'bootstrap setup list'), view='bootstrap_setup_list', icon=icon_bootstrap_setup, permissions=[PERMISSION_BOOTSTRAP_VIEW])
link_bootstrap_setup_create = Link(text=_(u'create new bootstrap setup'), view='bootstrap_setup_create', icon=icon_bootstrap_setup_create, permissions=[PERMISSION_BOOTSTRAP_CREATE])
link_bootstrap_setup_edit = Link(text=_(u'edit'), view='bootstrap_setup_edit', args='object.pk', icon=icon_bootstrap_setup_edit, permissions=[PERMISSION_BOOTSTRAP_EDIT])
link_bootstrap_setup_delete = Link(text=_(u'delete'), view='bootstrap_setup_delete', args='object.pk', icon=icon_bootstrap_setup_delete, permissions=[PERMISSION_BOOTSTRAP_DELETE])
link_bootstrap_setup_view = Link(text=_(u'details'), view='bootstrap_setup_view', args='object.pk', icon=icon_bootstrap_setup_view, permissions=[PERMISSION_BOOTSTRAP_VIEW])
link_bootstrap_setup_execute = Link(text=_(u'execute'), view='bootstrap_setup_execute', args='object.pk', icon=icon_bootstrap_setup_execute, permissions=[PERMISSION_BOOTSTRAP_EXECUTE])
link_bootstrap_setup_dump = Link(text=_(u'dump current setup'), view='bootstrap_setup_dump', icon=icon_bootstrap_setup_dump, permissions=[PERMISSION_BOOTSTRAP_DUMP])
link_erase_database = Link(text=_(u'erase database'), view='erase_database_view', icon=icon_nuke_database, permissions=[PERMISSION_NUKE_DATABASE])
