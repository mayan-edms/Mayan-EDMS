from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from mayan.apps.navigation.classes import Link

from .icons import (
    icon_document_submit, icon_document_multiple_submit, icon_file_metadata
)
from .permissions import (
    permission_document_type_file_metadata_setup,
    permission_file_metadata_submit, permission_file_metadata_view
)

link_document_driver_list = Link(
    icon_class=icon_file_metadata,
    kwargs={'document_id': 'resolved_object.id'},
    permissions=(permission_file_metadata_view,), text=_('File metadata'),
    view='file_metadata:document_driver_list'
)
link_document_file_metadata_list = Link(
    icon_class=icon_file_metadata,
    kwargs={'document_version_driver_id': 'resolved_object.id'},
    permissions=(permission_file_metadata_view,), text=_('Attributes'),
    view='file_metadata:document_version_driver_file_metadata_list'
)
link_document_submit = Link(
    icon_class=icon_document_submit,
    kwargs={'document_id': 'resolved_object.id'},
    permissions=(permission_file_metadata_submit,),
    text=_('Submit for file metadata'), view='file_metadata:document_submit'
)
link_document_multiple_submit = Link(
    icon_class=icon_document_multiple_submit, text=_('Submit for file metadata'),
    view='file_metadata:document_multiple_submit'
)
link_document_type_file_metadata_settings = Link(
    icon_class=icon_file_metadata,
    kwargs={'document_type_id': 'resolved_object.id'},
    permissions=(permission_document_type_file_metadata_setup,),
    text=_('Setup file metadata'), view='file_metadata:document_type_settings'
)
link_document_type_submit = Link(
    icon_class=icon_file_metadata,
    permissions=(permission_file_metadata_submit,),
    text=_('File metadata processing per type'),
    view='file_metadata:document_type_submit'
)
