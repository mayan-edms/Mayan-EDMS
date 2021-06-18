from django.utils.translation import ugettext_lazy as _

from mayan.apps.permissions import PermissionNamespace

namespace = PermissionNamespace(label=_('Mailing'), name='mailing')

permission_mailing_send_document_link = namespace.add_permission(
    label=_('Send document link via email'), name='mail_link'
)
permission_mailing_send_document_attachment = namespace.add_permission(
    label=_('Send document via email'), name='mail_document'
)
permission_user_mailer_create = namespace.add_permission(
    label=_('Create a mailing profile'), name='user_mailer_create'
)
permission_user_mailer_delete = namespace.add_permission(
    label=_('Delete a mailing profile'), name='user_mailer_delete'
)
permission_user_mailer_edit = namespace.add_permission(
    label=_('Edit a mailing profile'), name='user_mailer_edit'
)
permission_user_mailer_view = namespace.add_permission(
    label=_('View a mailing profile'), name='user_mailer_view'
)
permission_user_mailer_use = namespace.add_permission(
    label=_('Use a mailing profile'), name='user_mailer_use'
)
