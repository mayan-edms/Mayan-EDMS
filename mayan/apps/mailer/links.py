from django.utils.translation import ugettext_lazy as _

from mayan.apps.navigation.classes import Link

from .icons import (
    icon_document_file_attachment_send_single,
    icon_document_file_send_link_single,
    icon_document_file_attachment_send_multiple,
    icon_document_file_send_link_multiple,
    icon_document_send_link_single, icon_document_send_link_multiple,
    icon_document_version_send_attachment_single,
    icon_document_version_send_link_single,
    icon_document_version_send_link_multiple,
    icon_document_version_send_attachment_multiple, icon_user_mailer_create,
    icon_user_mailer_delete, icon_user_mailer_edit, icon_user_mailer_list,
    icon_user_mailer_setup, icon_user_mailer_test
)
from .permissions import (
    permission_send_document_file_attachment,
    permission_send_document_file_link,
    permission_send_document_version_attachment,
    permission_send_document_version_link, permission_send_document_link,
    permission_user_mailer_create, permission_user_mailer_delete,
    permission_user_mailer_edit, permission_user_mailer_use,
    permission_user_mailer_view
)

# Document

link_send_document_link_single = Link(
    args='resolved_object.pk', icon=icon_document_send_link_single,
    permissions=(permission_send_document_link,),
    text=_('Email document link'), view='mailer:send_document_link_single'
)
link_send_document_link_multiple = Link(
    icon=icon_document_send_link_multiple, text=_('Email document link'),
    view='mailer:send_document_link_multiple'
)

# Document file

link_send_document_file_attachment_single = Link(
    args='resolved_object.pk',
    icon=icon_document_file_attachment_send_single,
    permissions=(permission_send_document_file_attachment,),
    text=_('Email document file'),
    view='mailer:send_document_file_attachment_single'
)
link_send_document_file_attachment_multiple = Link(
    icon=icon_document_file_attachment_send_multiple,
    text=_('Email document file'),
    view='mailer:send_document_file_attachment_multiple'
)
link_send_document_file_link_single = Link(
    args='resolved_object.pk', icon=icon_document_file_send_link_single,
    permissions=(permission_send_document_file_link,),
    text=_('Email document file link'),
    view='mailer:send_document_file_link_single'
)
link_send_document_file_link_multiple = Link(
    icon=icon_document_file_send_link_multiple,
    text=_('Email document file link'),
    view='mailer:send_document_file_link_multiple'
)

# Document version

link_send_document_version_attachment_single = Link(
    args='resolved_object.pk',
    icon=icon_document_version_send_attachment_single,
    permissions=(permission_send_document_version_attachment,),
    text=_('Email document version'),
    view='mailer:send_document_version_attachment_single'
)
link_send_document_version_attachment_multiple = Link(
    icon=icon_document_version_send_attachment_multiple,
    text=_('Email document version'),
    view='mailer:send_document_version_attachment_multiple'
)
link_send_document_version_link_single = Link(
    args='resolved_object.pk', icon=icon_document_version_send_link_single,
    permissions=(permission_send_document_version_link,),
    text=_('Email document version link'),
    view='mailer:send_document_version_link_single'
)
link_send_document_version_link_multiple = Link(
    icon=icon_document_version_send_link_multiple,
    text=_('Email link version'),
    view='mailer:send_document_version_link_multiple'
)

# Mailing profile

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
