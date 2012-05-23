from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation.api import bind_links, register_sidebar_template, Link
from project_setup.api import register_setup
from documents.permissions import PERMISSION_DOCUMENT_VIEW
from documents.models import Document
from acls.api import class_permissions
from acls import ACLS_EDIT_ACL, ACLS_VIEW_ACL

from .models import SmartLink, SmartLinkCondition
from .permissions import (PERMISSION_SMART_LINK_VIEW,
    PERMISSION_SMART_LINK_CREATE, PERMISSION_SMART_LINK_DELETE,
    PERMISSION_SMART_LINK_EDIT)

smart_link_instance_view_link = Link(text=_(u'smart links actions'), view='smart_link_instance_view', sprite='page_link', permissions=[PERMISSION_DOCUMENT_VIEW])
smart_link_instances_for_document = Link(text=_(u'smart links'), view='smart_link_instances_for_document', args='object.pk', sprite='page_link', permissions=[PERMISSION_DOCUMENT_VIEW])

smart_link_setup = Link(text=_(u'smart links'), view='smart_link_list', icon='link.png', permissions=[PERMISSION_SMART_LINK_CREATE], children_view_regex=[r'smart_link_list', 'smart_link_create', 'smart_link_delete', 'smart_link_edit', 'smart_link_condition_'])
smart_link_list = Link(text=_(u'smart links list'), view='smart_link_list', sprite='link', permissions=[PERMISSION_SMART_LINK_CREATE])
smart_link_create = Link(text=_(u'create new smart link'), view='smart_link_create', sprite='link_add', permissions=[PERMISSION_SMART_LINK_CREATE])
smart_link_edit = Link(text=_(u'edit'), view='smart_link_edit', args='object.pk', sprite='link_edit', permissions=[PERMISSION_SMART_LINK_EDIT])
smart_link_delete = Link(text=_(u'delete'), view='smart_link_delete', args='object.pk', sprite='link_delete', permissions=[PERMISSION_SMART_LINK_DELETE])

smart_link_condition_list = Link(text=_(u'conditions'), view='smart_link_condition_list', args='object.pk', sprite='cog', permissions=[PERMISSION_SMART_LINK_CREATE, PERMISSION_SMART_LINK_CREATE])
smart_link_condition_create = Link(text=_(u'create condition'), view='smart_link_condition_create', args='object.pk', sprite='cog_add', permissions=[PERMISSION_SMART_LINK_CREATE, PERMISSION_SMART_LINK_EDIT])
smart_link_condition_edit = Link(text=_(u'edit'), view='smart_link_condition_edit', args='condition.pk', sprite='cog_edit', permissions=[PERMISSION_SMART_LINK_CREATE, PERMISSION_SMART_LINK_EDIT])
smart_link_condition_delete = Link(text=_(u'delete'), view='smart_link_condition_delete', args='condition.pk', sprite='cog_delete', permissions=[PERMISSION_SMART_LINK_CREATE, PERMISSION_SMART_LINK_EDIT])

smart_link_acl_list = Link(text=_(u'ACLs'), view='smart_link_acl_list', args='object.pk', sprite='lock', permissions=[ACLS_VIEW_ACL])

bind_links([Document], [smart_link_instances_for_document], menu_name='form_header')

bind_links([SmartLink], [smart_link_edit, smart_link_delete, smart_link_condition_list, smart_link_acl_list])
bind_links([SmartLink, 'smart_link_list', 'smart_link_create'], [smart_link_list, smart_link_create], menu_name='secondary_menu')

bind_links([SmartLinkCondition], [smart_link_condition_edit, smart_link_condition_delete])
bind_links(['smart_link_condition_list', 'smart_link_condition_create', 'smart_link_condition_edit', 'smart_link_condition_delete'], [smart_link_condition_create], menu_name='sidebar')

register_setup(smart_link_setup)
register_sidebar_template(['smart_link_list'], 'smart_links_help.html')

class_permissions(SmartLink, [
    PERMISSION_SMART_LINK_VIEW,
    PERMISSION_SMART_LINK_DELETE,
    PERMISSION_SMART_LINK_EDIT,
    ACLS_EDIT_ACL,
    ACLS_VIEW_ACL
])
