from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from mayan.apps.navigation.classes import Link
from mayan.apps.navigation.utils import get_cascade_condition

from .permissions import (
    permission_content_view, permission_document_type_parsing_setup,
    permission_parse_document
)


def is_document_page_disabled(context):
    return not context['resolved_object'].enabled


link_document_content = Link(
    args='resolved_object.id',
    icon_class_path='mayan.apps.document_parsing.icons.icon_document_content',
    permissions=(permission_content_view,), text=_('Content'),
    view='document_parsing:document_content'
)
link_document_page_content = Link(
    args='resolved_object.id', conditional_disable=is_document_page_disabled,
    icon_class_path='mayan.apps.document_parsing.icons.icon_document_content',
    permissions=(permission_content_view,), text=_('Content'),
    view='document_parsing:document_page_content'
)
link_document_parsing_errors_list = Link(
    args='resolved_object.id',
    icon_class_path='mayan.apps.document_parsing.icons.icon_document_parsing_errors_list',
    permissions=(permission_content_view,), text=_('Parsing errors'),
    view='document_parsing:document_parsing_error_list'
)
link_document_content_download = Link(
    args='resolved_object.id',
    icon_class_path='mayan.apps.document_parsing.icons.icon_document_content_download',
    permissions=(permission_content_view,), text=_('Download content'),
    view='document_parsing:document_content_download'
)
link_document_submit_multiple = Link(
    icon_class_path='mayan.apps.document_parsing.icons.icon_document_submit',
    text=_('Submit for parsing'),
    view='document_parsing:document_submit_multiple'
)
link_document_submit = Link(
    args='resolved_object.id',
    icon_class_path='mayan.apps.document_parsing.icons.icon_document_submit',
    permissions=(permission_parse_document,),
    text=_('Submit for parsing'), view='document_parsing:document_submit'
)
link_document_type_parsing_settings = Link(
    args='resolved_object.id',
    icon_class_path='mayan.apps.document_parsing.icons.icon_document_type_parsing_settings',
    permissions=(permission_document_type_parsing_setup,),
    text=_('Setup parsing'),
    view='document_parsing:document_type_parsing_settings'
)
link_document_type_submit = Link(
    condition=get_cascade_condition(
        app_label='documents', model_name='DocumentType',
        object_permission=permission_document_type_parsing_setup
    ),
    icon_class_path='mayan.apps.document_parsing.icons.icon_document_type_submit',
    text=_('Parse documents per type'),
    view='document_parsing:document_type_submit'
)
link_error_list = Link(
    icon_class_path='mayan.apps.document_parsing.icons.icon_link_error_list',
    permissions=(permission_content_view,), text=_('Parsing errors'),
    view='document_parsing:error_list'
)
