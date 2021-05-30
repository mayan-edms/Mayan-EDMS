from django.utils.translation import ugettext_lazy as _

from mayan.apps.navigation.classes import Link
from mayan.apps.navigation.utils import get_cascade_condition

from .icons import (
    icon_document_file_content, icon_document_file_content_delete,
    icon_document_file_content_download, icon_document_file_page_content,
    icon_document_file_parsing_errors_list, icon_document_file_submit,
    icon_document_type_parsing_settings, icon_document_type_submit,
    icon_error_list
)
from .permissions import (
    permission_document_file_content_view, permission_document_type_parsing_setup,
    permission_document_file_parse
)


link_document_file_content = Link(
    args='resolved_object.id', icon=icon_document_file_content,
    permissions=(permission_document_file_content_view,), text=_('Content'),
    view='document_parsing:document_file_content_view'
)
link_document_file_content_delete = Link(
    args='resolved_object.id', icon=icon_document_file_content_delete,
    permissions=(permission_document_file_parse,),
    text=_('Delete parsed content'),
    view='document_parsing:document_file_content_delete',
)
link_document_file_multiple_content_delete = Link(
    icon=icon_document_file_content_delete, text=_('Delete parsed content'),
    view='document_parsing:document_file_multiple_content_delete',
)
link_document_file_content_download = Link(
    args='resolved_object.id',
    icon=icon_document_file_content_download,
    permissions=(permission_document_file_content_view,), text=_('Download content'),
    view='document_parsing:document_file_content_download'
)
link_document_file_page_content = Link(
    args='resolved_object.id',
    icon=icon_document_file_page_content,
    permissions=(permission_document_file_content_view,), text=_('Content'),
    view='document_parsing:document_file_page_content_view'
)
link_document_file_parsing_errors_list = Link(
    args='resolved_object.id',
    icon=icon_document_file_parsing_errors_list,
    permissions=(permission_document_file_parse,), text=_('Parsing errors'),
    view='document_parsing:document_file_parsing_error_list'
)
link_document_file_multiple_submit = Link(
    icon=icon_document_file_submit,
    text=_('Submit for parsing'),
    view='document_parsing:document_file_multiple_submit'
)
link_document_file_submit = Link(
    args='resolved_object.id',
    icon=icon_document_file_submit,
    permissions=(permission_document_file_parse,),
    text=_('Submit for parsing'),
    view='document_parsing:document_file_submit'
)
link_document_type_parsing_settings = Link(
    args='resolved_object.id',
    icon=icon_document_type_parsing_settings,
    permissions=(permission_document_type_parsing_setup,),
    text=_('Setup parsing'),
    view='document_parsing:document_type_parsing_settings'
)
link_document_type_submit = Link(
    condition=get_cascade_condition(
        app_label='documents', model_name='DocumentType',
        object_permission=permission_document_type_parsing_setup
    ),
    icon=icon_document_type_submit,
    text=_('Parse documents per type'),
    view='document_parsing:document_type_submit'
)
link_error_list = Link(
    icon=icon_error_list,
    permissions=(permission_document_file_parse,), text=_('Parsing errors'),
    view='document_parsing:error_list'
)
