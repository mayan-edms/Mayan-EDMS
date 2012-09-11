from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from acls.api import class_permissions
from documents.models import Document
from navigation.api import bind_links, register_top_menu
from scheduler.api import LocalScheduler

from .permissions import (PERMISSION_DOCUMENT_CHECKOUT,
    PERMISSION_DOCUMENT_CHECKIN, PERMISSION_DOCUMENT_CHECKIN_OVERRIDE,
    PERMISSION_DOCUMENT_RESTRICTIONS_OVERRIDE)
from .links import checkout_list, checkout_document, checkout_info, checkin_document
from .models import DocumentCheckout
from .tasks import task_check_expired_check_outs
from .literals import CHECK_EXPIRED_CHECK_OUTS_INTERVAL


def initialize_document_checkout_extra_methods():
    Document.add_to_class('is_checked_out', lambda document: DocumentCheckout.objects.is_document_checked_out(document))
    Document.add_to_class('check_in', lambda document, user=None: DocumentCheckout.objects.check_in_document(document, user))
    Document.add_to_class('checkout_info', lambda document: DocumentCheckout.objects.document_checkout_info(document))
    Document.add_to_class('checkout_state', lambda document: DocumentCheckout.objects.document_checkout_state(document))
    Document.add_to_class('is_new_versions_allowed', lambda document, user=None: DocumentCheckout.objects.is_document_new_versions_allowed(document, user))

register_top_menu(name='checkouts', link=checkout_list)
bind_links([Document], [checkout_info], menu_name='form_header')
bind_links(['checkout_info', 'checkout_document', 'checkin_document'], [checkout_document, checkin_document], menu_name="sidebar")

class_permissions(Document, [
    PERMISSION_DOCUMENT_CHECKOUT,
    PERMISSION_DOCUMENT_CHECKIN,
    PERMISSION_DOCUMENT_CHECKIN_OVERRIDE,
    PERMISSION_DOCUMENT_RESTRICTIONS_OVERRIDE
])

checkouts_scheduler = LocalScheduler('checkouts', _(u'Document checkouts'))
checkouts_scheduler.add_interval_job('task_check_expired_check_outs', _(u'Check expired check out documents and checks them in.'), task_check_expired_check_outs, seconds=CHECK_EXPIRED_CHECK_OUTS_INTERVAL)
checkouts_scheduler.start()

initialize_document_checkout_extra_methods() 
