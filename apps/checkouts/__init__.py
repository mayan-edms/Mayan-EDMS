from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation.api import (register_links, register_top_menu,
    register_multi_item_links, register_sidebar_template)

from documents.models import Document
from documents.permissions import PERMISSION_DOCUMENT_VIEW
from acls.api import class_permissions

from .permissions import (PERMISSION_DOCUMENT_CHECKOUT, PERMISSION_DOCUMENT_CHECKIN, PERMISSION_DOCUMENT_CHECKIN_OVERRIDE)
from .links import checkout_list, checkout_document, checkout_info, checkin_document
from .models import DocumentCheckout


def initialize_document_checkout_extra_methods():
    Document.add_to_class('is_checked_out', lambda document: DocumentCheckout.objects.is_document_checked_out(document))
    Document.add_to_class('check_in', lambda document: DocumentCheckout.objects.check_in_document(document))
    Document.add_to_class('checkout_info', lambda document: DocumentCheckout.objects.document_checkout_info(document))
    Document.add_to_class('checkout_state', lambda document: DocumentCheckout.objects.document_checkout_state(document))
    Document.add_to_class('is_new_versions_allowed', lambda document: DocumentCheckout.objects.is_document_new_versions_allowed(document))

register_top_menu(name='checkouts', link=checkout_list)
register_links(Document, [checkout_info], menu_name='form_header')
register_links(['checkout_info', 'checkout_document', 'checkin_document'], [checkout_document, checkin_document], menu_name="sidebar")

class_permissions(Document, [
    PERMISSION_DOCUMENT_CHECKOUT,
    PERMISSION_DOCUMENT_CHECKIN,
    PERMISSION_DOCUMENT_CHECKIN_OVERRIDE
])

initialize_document_checkout_extra_methods()


#TODO: default checkout time
#TODO: forcefull check in
#TODO: specify checkout option check (document.allows_new_versions())
#TODO: out check in after expiration datetime
#TODO: add checkin out history
#TODO: limit restrictions to non checkout user and admins?
