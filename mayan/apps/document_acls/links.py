from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from acls.permissions import ACLS_VIEW_ACL

acl_list = {'text': _(u'ACLs'), 'view': 'document_acl_list', 'args': 'object.pk', 'famfam': 'lock', 'permissions': [ACLS_VIEW_ACL]}
