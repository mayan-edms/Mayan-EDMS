from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from .classes import LayerLink
from .layers import layer_saved_transformations


def conditional_active(context, resolved_link):
    return resolved_link.link.view == resolved_link.current_view_name and context.get('layer_name', None) == resolved_link.link.layer_name


link_transformation_delete = LayerLink(
    action='delete',
    kwargs={'layer_name': 'layer_name', 'pk': 'resolved_object.pk'},
    icon_class_path='mayan.apps.converter.icons.icon_transformation_delete',
    layer=layer_saved_transformations,
    tags='dangerous', text=_('Delete'), view='converter:transformation_delete'
)
link_transformation_edit = LayerLink(
    action='edit',
    kwargs={'layer_name': 'layer_name', 'pk': 'resolved_object.pk'},
    icon_class_path='mayan.apps.converter.icons.icon_transformation_edit',
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
