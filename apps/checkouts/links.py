from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from documents.permissions import PERMISSION_DOCUMENT_VIEW

from .permissions import (PERMISSION_DOCUMENT_CHECKOUT, PERMISSION_DOCUMENT_CHECKIN, PERMISSION_DOCUMENT_CHECKIN_OVERRIDE)


def is_checked_out(context):
    return context['object'].is_checked_out()


def is_not_checked_out(context):
    return not context['object'].is_checked_out()


checkout_list = {'text': _(u'checkouts'), 'view': 'checkout_list', 'famfam': 'basket'}
checkout_document = {'text': _('check out document'), 'view': 'checkout_document', 'args': 'object.pk', 'famfam': 'basket_put', 'condition': is_not_checked_out, 'permissions': [PERMISSION_DOCUMENT_CHECKOUT]}
checkin_document = {'text': _('check in document'), 'view': 'checkin_document', 'args': 'object.pk', 'famfam': 'basket_remove', 'condition': is_checked_out, 'permissions': [PERMISSION_DOCUMENT_CHECKIN, PERMISSION_DOCUMENT_CHECKIN_OVERRIDE]}
checkout_info = {'text': _('check in/out'), 'view': 'checkout_info', 'args': 'object.pk', 'famfam': 'basket', 'children_views': ['checkout_document', 'checkin_document'], 'permissions': [PERMISSION_DOCUMENT_CHECKIN, PERMISSION_DOCUMENT_CHECKIN_OVERRIDE, PERMISSION_DOCUMENT_CHECKOUT]}
