from django.utils.translation import ugettext_lazy as _

from mayan.apps.permissions import PermissionNamespace

namespace = PermissionNamespace(
    label=_('Document parsing'), name='document_parsing'
)

permission_document_file_content_view = namespace.add_permission(
    label=_('View the content of a document file'), name='content_view'
)
permission_document_file_parse = namespace.add_permission(
    label=_('Parse the content of a document file'), name='parse_document'
)
permission_document_type_parsing_setup = namespace.add_permission(
    label=_('Change document type parsing settings'),
    name='document_type_setup'
)
