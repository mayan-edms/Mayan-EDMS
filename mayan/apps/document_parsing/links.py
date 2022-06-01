from django.utils.translation import ugettext_lazy as _

from mayan.apps.navigation.classes import Link
from mayan.apps.navigation.utils import factory_condition_queryset_access

from .icons import (
    icon_document_file_content_detail,
    icon_document_file_content_single_delete,
    icon_document_file_content_multiple_delete,
    icon_document_file_content_download,
    icon_document_file_page_content_detail,
    icon_document_file_parsing_multiple_submit,
    icon_document_type_parsing_settings,
    icon_document_file_parsing_single_submit,
    icon_document_type_parsing_submit
)
from .permissions import (
    permission_document_file_content_view, permission_document_type_parsing_setup,
    permission_document_file_parse
)

# Document file

link_document_file_content_detail = Link(
    args='resolved_object.id', icon=icon_document_file_content_detail,
    permissions=(permission_document_file_content_view,), text=_('Content'),
    view='document_parsing:document_file_content_view'
)
link_document_file_content_single_delete = Link(
    args='resolved_object.id', icon=icon_document_file_content_single_delete,
    permissions=(permission_document_file_parse,),
    text=_('Delete parsed content'),
    view='document_parsing:document_file_content_single_delete',
)
link_document_file_content_multiple_delete = Link(
    icon=icon_document_file_content_multiple_delete,
    text=_('Delete parsed content'),
    view='document_parsing:document_file_content_multiple_delete',
)
link_document_file_content_download = Link(
    args='resolved_object.id', icon=icon_document_file_content_download,
    permissions=(permission_document_file_content_view,),
    text=_('Download content'),
    view='document_parsing:document_file_content_download'
)
link_document_file_page_content_detail = Link(
    args='resolved_object.id',
    icon=icon_document_file_page_content_detail,
    permissions=(permission_document_file_content_view,), text=_('Content'),
    view='document_parsing:document_file_page_content_view'
)
link_document_file_parsing_multiple_submit = Link(
    icon=icon_document_file_parsing_multiple_submit,
    text=_('Submit for parsing'),
    view='document_parsing:document_file_parsing_multiple_submit'
)
link_document_file_parsing_single_submit = Link(
    args='resolved_object.id',
    icon=icon_document_file_parsing_single_submit,
    permissions=(permission_document_file_parse,),
    text=_('Submit for parsing'),
    view='document_parsing:document_file_parsing_single_submit'
)

# Document type

link_document_type_parsing_settings = Link(
    args='resolved_object.id',
    icon=icon_document_type_parsing_settings,
    permissions=(permission_document_type_parsing_setup,),
    text=_('Setup parsing'),
    view='document_parsing:document_type_parsing_settings'
)
link_document_type_parsing_submit = Link(
    condition=factory_condition_queryset_access(
        app_label='documents', model_name='DocumentType',
        object_permission=permission_document_type_parsing_setup
    ),
    icon=icon_document_type_parsing_submit,
    text=_('Parse documents per type'),
    view='document_parsing:document_type_submit'
)
