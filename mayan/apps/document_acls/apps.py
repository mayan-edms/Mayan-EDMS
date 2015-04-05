from __future__ import unicode_literals

from django import apps
from django.utils.translation import ugettext_lazy as _

from acls.api import class_permissions
from acls.permissions import ACLS_VIEW_ACL, ACLS_EDIT_ACL
from common import menu_facet
from documents.models import Document

from .links import link_acl_list


class DocumentACLsApp(apps.AppConfig):
    name = 'document_acls'
    verbose_name = _('Document ACLs')

    def ready(self):
        class_permissions(Document, [
            ACLS_VIEW_ACL,
            ACLS_EDIT_ACL
        ])

        menu_facet.bind_links(links=[link_acl_list], sources=[Document])
