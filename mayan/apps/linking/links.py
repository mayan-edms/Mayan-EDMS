from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from acls.permissions import ACLS_VIEW_ACL
from documents.permissions import PERMISSION_DOCUMENT_VIEW
from navigation import Link

from .permissions import (
    PERMISSION_SMART_LINK_CREATE, PERMISSION_SMART_LINK_DELETE,
    PERMISSION_SMART_LINK_EDIT, PERMISSION_SMART_LINK_VIEW
)

link_smart_link_acl_list = Link(permissions=[ACLS_VIEW_ACL], text=_('ACLs'), view='linking:smart_link_acl_list', args='object.pk')
link_smart_link_condition_create = Link(permissions=[PERMISSION_SMART_LINK_EDIT], text=_('Create condition'), view='linking:smart_link_condition_create', args='object.pk')
link_smart_link_condition_delete = Link(permissions=[PERMISSION_SMART_LINK_EDIT], text=_('Delete'), view='linking:smart_link_condition_delete', args='condition.pk')
link_smart_link_condition_edit = Link(permissions=[PERMISSION_SMART_LINK_EDIT], text=_('Edit'), view='linking:smart_link_condition_edit', args='condition.pk')
link_smart_link_condition_list = Link(permissions=[PERMISSION_SMART_LINK_EDIT], text=_('Conditions'), view='linking:smart_link_condition_list', args='object.pk')
link_smart_link_create = Link(permissions=[PERMISSION_SMART_LINK_CREATE], text=_('Create new smart link'), view='linking:smart_link_create')
link_smart_link_delete = Link(permissions=[PERMISSION_SMART_LINK_DELETE], text=_('Delete'), view='linking:smart_link_delete', args='object.pk')
link_smart_link_document_types = Link(permissions=[PERMISSION_SMART_LINK_EDIT], text=_('Document types'), view='linking:smart_link_document_types', args='object.pk')
link_smart_link_edit = Link(permissions=[PERMISSION_SMART_LINK_EDIT], text=_('Edit'), view='linking:smart_link_edit', args='object.pk')
link_smart_link_instance_view = Link(permissions=[PERMISSION_SMART_LINK_VIEW], text=_('Documents'), view='linking:smart_link_instance_view', args=['document.pk', 'object.smart_link.pk'])
link_smart_link_instances_for_document = Link(permissions=[PERMISSION_DOCUMENT_VIEW], text=_('Smart links'), view='linking:smart_link_instances_for_document', args='object.pk')
link_smart_link_list = Link(permissions=[PERMISSION_SMART_LINK_CREATE], text=_('Smart links'), view='linking:smart_link_list')
link_smart_link_setup = Link(icon='fa fa-link', permissions=[PERMISSION_SMART_LINK_CREATE], text=_('Smart links'), view='linking:smart_link_list')
