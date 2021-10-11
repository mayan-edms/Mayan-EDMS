from django.utils.translation import ugettext_lazy as _

from mayan.apps.navigation.classes import Link

from .icons import (
    icon_document_file_submit_single, icon_document_file_submit_multiple,
    icon_document_type_submit, icon_file_metadata
)
from .permissions import (
    permission_document_type_file_metadata_setup,
    permission_file_metadata_submit, permission_file_metadata_view
)

# Document file

link_document_file_metadata_driver_list = Link(
    icon=icon_file_metadata,
    kwargs={'document_file_id': 'resolved_object.id'},
    permissions=(permission_file_metadata_view,), text=_('File metadata'),
    view='file_metadata:document_file_driver_list'
)
link_document_file_metadata_list = Link(
    icon=icon_file_metadata,
    kwargs={'document_file_driver_id': 'resolved_object.id'},
    permissions=(permission_file_metadata_view,), text=_('Attributes'),
    view='file_metadata:document_file_driver_file_metadata_list'
)
link_document_file_metadata_submit_single = Link(
    icon=icon_document_file_submit_single,
    kwargs={'document_file_id': 'resolved_object.id'},
    permissions=(permission_file_metadata_submit,),
    text=_('Submit for file metadata'),
    view='file_metadata:document_file_submit_single'
)
link_document_file_metadata_submit_multiple = Link(
    icon=icon_document_file_submit_multiple,
    text=_('Submit for file metadata'),
    view='file_metadata:document_file_submit_multiple'
)

# Document type

link_document_type_file_metadata_settings = Link(
    icon=icon_file_metadata,
    kwargs={'document_type_id': 'resolved_object.id'},
    permissions=(permission_document_type_file_metadata_setup,),
    text=_('Setup file metadata'), view='file_metadata:document_type_settings'
)
link_document_type_submit = Link(
    icon=icon_document_type_submit,
    permissions=(permission_file_metadata_submit,),
    text=_('File metadata processing per type'),
    view='file_metadata:document_type_submit'
)
