from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from navigation import Link

from .permissions import (
    PERMISSION_DOCUMENT_CHECKOUT, PERMISSION_DOCUMENT_CHECKIN,
    PERMISSION_DOCUMENT_CHECKIN_OVERRIDE
)


def is_checked_out(context):
    return context['object'].is_checked_out()


def is_not_checked_out(context):
    return not context['object'].is_checked_out()


link_checkout_list = Link(icon='fa fa-shopping-cart', text=_('Checkouts'), view='checkouts:checkout_list')
link_checkout_document = Link(condition=is_not_checked_out, permissions=[PERMISSION_DOCUMENT_CHECKOUT], text=_('Check out document'), view='checkouts:checkout_document', args='object.pk')
link_checkin_document = Link(condition=is_checked_out, permissions=[PERMISSION_DOCUMENT_CHECKIN, PERMISSION_DOCUMENT_CHECKIN_OVERRIDE], text=_('Check in document'), view='checkouts:checkin_document', args='object.pk')
link_checkout_info = Link(permissions=[PERMISSION_DOCUMENT_CHECKIN, PERMISSION_DOCUMENT_CHECKIN_OVERRIDE, PERMISSION_DOCUMENT_CHECKOUT], text=_('Check in/out'), view='checkouts:checkout_info', args='object.pk')
