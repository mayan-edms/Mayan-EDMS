from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from acls.permissions import ACLS_VIEW_ACL
from navigation import Link

link_acl_list = Link(permissions=[ACLS_VIEW_ACL], text=_('ACLs'), view='document_acls:document_acl_list', args='object.pk')
