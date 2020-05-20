from django.utils.translation import ugettext_lazy as _

from mayan.apps.navigation.classes import Link

from .icons import (
    icon_check_in_document, icon_check_out_document, icon_check_out_info
)
from .permissions import (
    permission_document_check_out, permission_document_check_in,
    permission_document_check_in_override,
    permission_document_check_out_detail_view
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


link_check_out_list = Link(
    icon_class=icon_check_out_info, text=_('Checkouts'),
    view='checkouts:check_out_list'
)
link_check_out_document = Link(
    args='object.pk', condition=is_not_checked_out,
    icon_class=icon_check_out_document,
    permissions=(permission_document_check_out,),
    text=_('Check out document'), view='checkouts:check_out_document'
)
link_check_out_document_multiple = Link(
    icon_class=icon_check_out_document,
    permissions=(permission_document_check_out,), text=_('Check out'),
    view='checkouts:check_out_document_multiple'
)
link_check_in_document = Link(
    args='object.pk', icon_class=icon_check_in_document,
    condition=is_checked_out, permissions=(
        permission_document_check_in, permission_document_check_in_override
    ), text=_('Check in document'), view='checkouts:check_in_document'
)
link_check_in_document_multiple = Link(
    icon_class=icon_check_in_document,
    permissions=(permission_document_check_in,), text=_('Check in'),
    view='checkouts:check_in_document_multiple'
)
link_check_out_info = Link(
    args='resolved_object.pk', icon_class=icon_check_out_info, permissions=(
        permission_document_check_out_detail_view,
    ), text=_('Check in/out'), view='checkouts:check_out_info'
)
