from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation import Link

from .permissions import (PERMISSION_DOCUMENT_CHECKOUT, PERMISSION_DOCUMENT_CHECKIN, PERMISSION_DOCUMENT_CHECKIN_OVERRIDE)


def is_checked_out(context):
    return context['object'].is_checked_out()


def is_not_checked_out(context):
    return not context['object'].is_checked_out()


checkout_list = Link(text=_(u'checkouts'), view='checkout_list', sprite='basket')
checkout_document = Link(text=_('check out document'), view='checkout_document', args='object.pk', sprite='basket_put', condition=is_not_checked_out, permissions=[PERMISSION_DOCUMENT_CHECKOUT])
checkin_document = Link(text=_('check in document'), view='checkin_document', args='object.pk', sprite='basket_remove', condition=is_checked_out, permissions=[PERMISSION_DOCUMENT_CHECKIN, PERMISSION_DOCUMENT_CHECKIN_OVERRIDE])
checkout_info = Link(text=_('check in/out'), view='checkout_info', args='object.pk', sprite='basket', children_views=['checkout_document', 'checkin_document'], permissions=[PERMISSION_DOCUMENT_CHECKIN, PERMISSION_DOCUMENT_CHECKIN_OVERRIDE, PERMISSION_DOCUMENT_CHECKOUT])
