from django.utils.translation import ugettext_lazy as _

from mayan.apps.navigation.classes import Link
from mayan.apps.navigation.utils import get_cascade_condition

from .classes import LayerLink
from .layers import layer_saved_transformations
from .transformations import BaseTransformation
from .permissions import (
    permission_asset_create, permission_asset_delete,
    permission_asset_edit, permission_asset_view
)


def conditional_active(context, resolved_link):
    return resolved_link.link.view == resolved_link.current_view_name and context.get('layer_name', None) == resolved_link.link.layer_name


def condition_valid_transformation_and_arguments(context):
    try:
        transformation = BaseTransformation.get(name=context['object'].name)
    except KeyError:
        return False
    else:
        return transformation.arguments


link_asset_create = Link(
    icon_class_path='mayan.apps.converter.icons.icon_asset_create',
    permissions=(permission_asset_create,),
    text=_('Create asset'), view='converter:asset_create'
)
link_asset_multiple_delete = Link(
    icon_class_path='mayan.apps.converter.icons.icon_asset_delete',
    tags='dangerous', text=_('Delete'), view='converter:asset_multiple_delete'
)
link_asset_single_delete = Link(
    args='object.pk',
    icon_class_path='mayan.apps.converter.icons.icon_asset_delete',
    permissions=(permission_asset_delete,),
    tags='dangerous', text=_('Delete'), view='converter:asset_single_delete'
)
link_asset_edit = Link(
    args='object.pk',
    icon_class_path='mayan.apps.converter.icons.icon_asset_edit',
    permissions=(permission_asset_edit,), text=_('Edit'),
    view='converter:asset_edit'
)
link_asset_list = Link(
    condition=get_cascade_condition(
        app_label='converter', model_name='Asset',
        object_permission=permission_asset_view,
        view_permission=permission_asset_create,
    ), icon_class_path='mayan.apps.converter.icons.icon_asset_list',
    text=_('Assets'),
    view='converter:asset_list'
)

link_transformation_delete = LayerLink(
    action='delete', kwargs={
        'layer_name': 'layer_name', 'transformation_id': 'resolved_object.pk'
    },
    icon_class_path='mayan.apps.converter.icons.icon_transformation_delete',
    layer=layer_saved_transformations,
    tags='dangerous', text=_('Delete'), view='converter:transformation_delete'
)
link_transformation_edit = LayerLink(
    action='edit', condition=condition_valid_transformation_and_arguments,
    kwargs={
        'layer_name': 'layer_name', 'transformation_id': 'resolved_object.pk'
    }, icon_class_path='mayan.apps.converter.icons.icon_transformation_edit',
    layer=layer_saved_transformations,
    text=_('Edit'), view='converter:transformation_edit'
)
link_transformation_list = LayerLink(
    action='list', conditional_active=conditional_active,
    layer=layer_saved_transformations, text=_('Transformations'),
    view='converter:transformation_list'
)
link_transformation_select = LayerLink(
    action='select',
    icon_class_path='mayan.apps.converter.icons.icon_transformation_select',
    layer=layer_saved_transformations, text=_('Select new transformation'),
    view='converter:transformation_select'
)
