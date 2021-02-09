from django.utils.translation import ugettext_lazy as _

from mayan.apps.navigation.classes import Link

from .icons import icon_template_sandbox
from .permissions import permission_template_sandbox


link_document_template_sandbox = Link(
    args='resolved_object.pk', icon=icon_template_sandbox,
    permissions=(permission_template_sandbox,), text=_('Sandbox'),
    view='templating:document_template_sandbox'
)
