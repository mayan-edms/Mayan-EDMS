from __future__ import unicode_literals

from django import apps
from django.utils.translation import ugettext_lazy as _

from acls.api import class_permissions
from acls.permissions import ACLS_VIEW_ACL, ACLS_EDIT_ACL
from documents.models import Document

from .links import acl_list


class DocumentACLsApp(apps.AppConfig):
    name = 'document_acls'
    verbose_name = _('Document ACLs')

    def ready(self):
        #TODO: convert
        #register_links(Document, [acl_list], menu_name='form_header')

        class_permissions(Document, [
            ACLS_VIEW_ACL,
            ACLS_EDIT_ACL
        ])
