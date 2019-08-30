from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from mayan.apps.documents.permissions import permission_document_type_edit
from mayan.apps.navigation.classes import Link

from .icons import icon_control_code
from .permissions import (
    permission_web_link_create, permission_web_link_delete,
    permission_web_link_edit, permission_web_link_instance_view,
)

link_control_code_tools = Link(
    icon_class=icon_control_code, text=_('Control codes'),
    view='control_codes:control_code_create'
)
