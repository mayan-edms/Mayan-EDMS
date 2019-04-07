from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from navigation import Link

from .icons import icon_checkout_info
from .permissions import (
    permission_document_checkout, permission_document_checkin,
    permission_document_checkin_override,
    permission_document_checkout_detail_view
)


def is_checked_out(context):
    try:
        return context['object'].is_checked_out()
    except KeyError:
        # Might not have permissions
        return False


def is_not_checked_out(context):
    try:
        return not context['object'].is_checked_out()
    except KeyError:
        # Might not have permissions
        return True


link_checkout_list = Link(
    icon_class=icon_checkout_info, text=_('Checkouts'),
    view='checkouts:checkout_list'
)
link_checkout_document = Link(
    args='object.pk', condition=is_not_checked_out,
    permissions=(permission_document_checkout,),
    text=_('Check out document'), view='checkouts:checkout_document',
)
link_checkin_document = Link(
    args='object.pk', condition=is_checked_out, permissions=(
        permission_document_checkin, permission_document_checkin_override
    ), text=_('Check in document'), view='checkouts:checkin_document',
)
link_checkout_info = Link(
    args='resolved_object.pk', icon_class=icon_checkout_info, permissions=(
        permission_document_checkout_detail_view,
    ), text=_('Check in/out'), view='checkouts:checkout_info',
)
