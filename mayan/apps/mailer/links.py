from django.utils.translation import ugettext_lazy as _

from mayan.apps.navigation.classes import Link

from .icons import (
    icon_document_send, icon_document_send_link, icon_user_mailer_create,
    icon_user_mailer_delete, icon_user_mailer_edit, icon_user_mailer_list,
    icon_user_mailer_setup, icon_user_mailer_test
)
from .permissions import (
    permission_mailing_link, permission_mailing_send_document,
    permission_user_mailer_create, permission_user_mailer_delete,
    permission_user_mailer_edit, permission_user_mailer_use,
    permission_user_mailer_view
)

link_send_document = Link(
    args='resolved_object.pk', icon=icon_document_send,
    permissions=(permission_mailing_send_document,),
    text=_('Email document'), view='mailer:send_document'
)
link_send_document_link = Link(
    args='resolved_object.pk', icon=icon_document_send_link,
    permissions=(permission_mailing_link,),
    text=_('Email link'), view='mailer:send_document_link'
)
link_send_multiple_document = Link(
    icon=icon_document_send, text=_('Email document'),
    view='mailer:send_multiple_document'
)
link_send_multiple_document_link = Link(
    icon=icon_document_send_link, text=_('Email link'),
    view='mailer:send_multiple_document_link'
)
link_user_mailer_create = Link(
    icon=icon_user_mailer_create,
    permissions=(permission_user_mailer_create,),
    text=_('Create mailing profile'),
    view='mailer:user_mailer_backend_selection'
)
link_user_mailer_delete = Link(
    args='resolved_object.pk', icon=icon_user_mailer_delete,
    permissions=(permission_user_mailer_delete,), tags='dangerous',
    text=_('Delete'), view='mailer:user_mailer_delete'
)
link_user_mailer_edit = Link(
    args='object.pk', icon=icon_user_mailer_edit,
    permissions=(permission_user_mailer_edit,), text=_('Edit'),
    view='mailer:user_mailer_edit'
)
link_user_mailer_list = Link(
    icon=icon_user_mailer_list,
    permissions=(permission_user_mailer_view,),
    text=_('Mailing profiles list'), view='mailer:user_mailer_list'
)
link_user_mailer_setup = Link(
    icon=icon_user_mailer_setup,
    permissions=(permission_user_mailer_view,), text=_('Mailing profiles'),
    view='mailer:user_mailer_list'
)
link_user_mailer_test = Link(
    args='object.pk', icon=icon_user_mailer_test,
    permissions=(permission_user_mailer_use,), text=_('Test'),
    view='mailer:user_mailer_test'
)
