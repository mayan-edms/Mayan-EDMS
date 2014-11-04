from __future__ import absolute_import

from datetime import timedelta

from acls.api import class_permissions
from documents.models import Document
from mayan.celery import app
from history.api import register_history_type
from navigation.api import register_links, register_top_menu
from rest_api.classes import APIEndPoint

from .events import (HISTORY_DOCUMENT_AUTO_CHECKED_IN,
                     HISTORY_DOCUMENT_CHECKED_OUT,
                     HISTORY_DOCUMENT_CHECKED_IN,
                     HISTORY_DOCUMENT_FORCEFUL_CHECK_IN)
from .links import (checkin_document, checkout_document, checkout_info,
                    checkout_list)
from .models import DocumentCheckout
from .permissions import (PERMISSION_DOCUMENT_CHECKIN,
                          PERMISSION_DOCUMENT_CHECKIN_OVERRIDE,
                          PERMISSION_DOCUMENT_CHECKOUT,
                          PERMISSION_DOCUMENT_RESTRICTIONS_OVERRIDE)

CHECK_EXPIRED_CHECK_OUTS_INTERVAL = 60  # Lowest check out expiration allowed


def initialize_document_checkout_extra_methods():
    Document.add_to_class('is_checked_out', lambda document: DocumentCheckout.objects.is_document_checked_out(document))
    Document.add_to_class('check_in', lambda document, user=None: DocumentCheckout.objects.check_in_document(document, user))
    Document.add_to_class('checkout_info', lambda document: DocumentCheckout.objects.document_checkout_info(document))
    Document.add_to_class('checkout_state', lambda document: DocumentCheckout.objects.document_checkout_state(document))
    Document.add_to_class('is_new_versions_allowed', lambda document, user=None: DocumentCheckout.objects.is_document_new_versions_allowed(document, user))


app.conf.CELERYBEAT_SCHEDULE.update({
    'check_expired_check_outs': {
        'task': 'checkouts.tasks.task_check_expired_check_outs',
        'schedule': timedelta(seconds=CHECK_EXPIRED_CHECK_OUTS_INTERVAL),
        'options': {'queue': 'checkouts'}
    },
})

class_permissions(Document, [
    PERMISSION_DOCUMENT_CHECKOUT,
    PERMISSION_DOCUMENT_CHECKIN,
    PERMISSION_DOCUMENT_CHECKIN_OVERRIDE,
    PERMISSION_DOCUMENT_RESTRICTIONS_OVERRIDE
])

initialize_document_checkout_extra_methods()
register_history_type(HISTORY_DOCUMENT_CHECKED_OUT)
register_history_type(HISTORY_DOCUMENT_CHECKED_IN)
register_history_type(HISTORY_DOCUMENT_AUTO_CHECKED_IN)
register_history_type(HISTORY_DOCUMENT_FORCEFUL_CHECK_IN)

register_links(Document, [checkout_info], menu_name='form_header')
register_links(['checkouts:checkout_info', 'checkouts:checkout_document', 'checkouts:checkin_document'], [checkout_document, checkin_document], menu_name="sidebar")
register_top_menu(name='checkouts', link=checkout_list)

APIEndPoint('checkouts')
