from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation.api import Link
from documents.permissions import PERMISSION_DOCUMENT_VIEW
from acls.permissions import ACLS_VIEW_ACL

from .permissions import (PERMISSION_SMART_LINK_CREATE,
    PERMISSION_SMART_LINK_DELETE, PERMISSION_SMART_LINK_EDIT)

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
