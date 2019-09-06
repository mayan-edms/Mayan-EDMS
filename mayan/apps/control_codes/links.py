from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from mayan.apps.navigation.classes import Link

from .permissions import (
    permission_control_sheet_create, permission_control_sheet_delete,
    permission_control_sheet_edit, permission_control_sheet_view,
)

link_control_sheet_create = Link(
    icon_class_path='mayan.apps.control_codes.icons.icon_control_sheet_create',
    text=_('Create control sheet'), permissions=(permission_control_sheet_create,),
    view='control_codes:control_sheet_create'
)
link_control_sheet_delete = Link(
    icon_class_path='mayan.apps.control_codes.icons.icon_control_sheet_delete',
    kwargs={'control_sheet_id': 'resolved_object.pk'}, text=_('Delete'),
    permissions=(permission_control_sheet_delete,), tags='dangerous',
    view='control_codes:control_sheet_delete'
)
link_control_sheet_edit = Link(
    icon_class_path='mayan.apps.control_codes.icons.icon_control_sheet_edit',
    kwargs={'control_sheet_id': 'resolved_object.pk'}, text=_('Edit'),
    permissions=(permission_control_sheet_edit,),
    view='control_codes:control_sheet_edit'
)
link_control_sheet_list = Link(
    icon_class_path='mayan.apps.control_codes.icons.icon_control_sheet_list',
    text=_('Control sheets'), view='control_codes:control_sheet_list'
)
link_control_sheet_preview = Link(
    icon_class_path='mayan.apps.control_codes.icons.icon_control_sheet_preview',
    kwargs={'control_sheet_id': 'resolved_object.pk'},
    text=_('Preview'), permissions=(permission_control_sheet_view,),
    view='control_codes:control_sheet_preview'
)
link_control_sheet_print = Link(
    icon_class_path='mayan.apps.control_codes.icons.icon_control_sheet_print',
    kwargs={'control_sheet_id': 'resolved_object.pk'},
    text=_('Print'), permissions=(permission_control_sheet_view,),
    view='control_codes:control_sheet_print'
)

link_control_sheet_code_select = Link(
    icon_class_path='mayan.apps.control_codes.icons.icon_control_sheet_code_select',
    kwargs={'control_sheet_id': 'control_sheet.pk'}, text=_('Add new code'),
    permissions=(permission_control_sheet_edit,),
    view='control_codes:control_sheet_code_select'
)
link_control_sheet_code_delete = Link(
    icon_class_path='mayan.apps.control_codes.icons.icon_control_sheet_code_delete',
    kwargs={
        'control_sheet_id': 'control_sheet.pk',
        'control_sheet_code_id': 'resolved_object.pk'
    }, tags='dangerous', text=_('Delete'),
    permissions=(permission_control_sheet_delete,),
    view='control_codes:control_sheet_code_delete'
)
link_control_sheet_code_edit = Link(
    icon_class_path='mayan.apps.control_codes.icons.icon_control_sheet_code_edit',
    kwargs={
        'control_sheet_id': 'control_sheet.pk',
        'control_sheet_code_id': 'resolved_object.pk'
    }, text=_('Edit'), permissions=(permission_control_sheet_edit,),
    view='control_codes:control_sheet_code_edit'
)
link_control_sheet_code_list = Link(
    icon_class_path='mayan.apps.control_codes.icons.icon_control_sheet_code_list',
    kwargs={'control_sheet_id': 'resolved_object.pk'},
    text=_('Codes'), permissions=(permission_control_sheet_view,),
    view='control_codes:control_sheet_code_list'
)
