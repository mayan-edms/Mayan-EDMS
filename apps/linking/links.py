from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation import Link
from documents.permissions import PERMISSION_DOCUMENT_VIEW
from acls.permissions import ACLS_VIEW_ACL

from .permissions import (PERMISSION_SMART_LINK_CREATE,
    PERMISSION_SMART_LINK_DELETE, PERMISSION_SMART_LINK_EDIT)
from .icons import (icon_smart_link_instance_view, icon_smart_link_instances_for_document,
    icon_smart_link_setup, icon_smart_link_list, icon_smart_link_create,
    icon_smart_link_edit, icon_smart_link_delete, icon_smart_link_condition_list,
    icon_smart_link_condition_create, icon_smart_link_condition_edit,
    icon_smart_link_condition_delete, icon_smart_link_acl_list)

smart_link_instance_view_link = Link(text=_(u'smart links actions'), view='smart_link_instance_view', icon=icon_smart_link_instance_view, permissions=[PERMISSION_DOCUMENT_VIEW])
smart_link_instances_for_document = Link(text=_(u'smart links'), view='smart_link_instances_for_document', args='object.pk', icon=icon_smart_link_instances_for_document, permissions=[PERMISSION_DOCUMENT_VIEW])

smart_link_setup = Link(text=_(u'smart links'), view='smart_link_list', icon=icon_smart_link_setup, permissions=[PERMISSION_SMART_LINK_CREATE], children_view_regex=[r'smart_link_list', 'smart_link_create', 'smart_link_delete', 'smart_link_edit', 'smart_link_condition_'])
smart_link_list = Link(text=_(u'smart links list'), view='smart_link_list', icon=icon_smart_link_list, permissions=[PERMISSION_SMART_LINK_CREATE])
smart_link_create = Link(text=_(u'create new smart link'), view='smart_link_create', icon=icon_smart_link_create, permissions=[PERMISSION_SMART_LINK_CREATE])
smart_link_edit = Link(text=_(u'edit'), view='smart_link_edit', args='object.pk', icon=icon_smart_link_edit, permissions=[PERMISSION_SMART_LINK_EDIT])
smart_link_delete = Link(text=_(u'delete'), view='smart_link_delete', args='object.pk', icon=icon_smart_link_delete, permissions=[PERMISSION_SMART_LINK_DELETE])

smart_link_condition_list = Link(text=_(u'conditions'), view='smart_link_condition_list', args='object.pk', icon=icon_smart_link_condition_list, permissions=[PERMISSION_SMART_LINK_CREATE, PERMISSION_SMART_LINK_CREATE])
smart_link_condition_create = Link(text=_(u'create condition'), view='smart_link_condition_create', args='object.pk', icon=icon_smart_link_condition_create, permissions=[PERMISSION_SMART_LINK_CREATE, PERMISSION_SMART_LINK_EDIT])
smart_link_condition_edit = Link(text=_(u'edit'), view='smart_link_condition_edit', args='condition.pk', icon=icon_smart_link_condition_edit, permissions=[PERMISSION_SMART_LINK_CREATE, PERMISSION_SMART_LINK_EDIT])
smart_link_condition_delete = Link(text=_(u'delete'), view='smart_link_condition_delete', args='condition.pk', icon=icon_smart_link_condition_delete, permissions=[PERMISSION_SMART_LINK_CREATE, PERMISSION_SMART_LINK_EDIT])

smart_link_acl_list = Link(text=_(u'ACLs'), view='smart_link_acl_list', args='object.pk', icon=icon_smart_link_acl_list, permissions=[ACLS_VIEW_ACL])
