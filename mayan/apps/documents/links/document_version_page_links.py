from django.utils.translation import ugettext_lazy as _

from mayan.apps.navigation.classes import Link

from ..icons import (
    icon_document_page_navigation_first,
    icon_document_page_navigation_last, icon_document_page_navigation_next,
    icon_document_page_navigation_previous, icon_document_page_return,
    icon_document_page_rotate_left, icon_document_page_rotate_right,
    icon_document_page_zoom_in, icon_document_page_zoom_out,
)
from ..permissions import (
    permission_document_edit, permission_document_tools,
    permission_document_view
)
from ..settings import setting_zoom_max_level, setting_zoom_min_level


def is_first_page(context):
    return context['resolved_object'].siblings.first() == context['resolved_object']


def is_last_page(context):
    return context['resolved_object'].siblings.last() == context['resolved_object']


def is_max_zoom(context):
    return context['zoom'] >= setting_zoom_max_level.value


def is_min_zoom(context):
    return context['zoom'] <= setting_zoom_min_level.value


def is_document_page_enabled(context):
    return context['resolved_object'].enabled


def is_document_page_disabled(context):
    return not context['resolved_object'].enabled


link_document_page_disable = Link(
    condition=is_document_page_enabled,
    icon_class_path='mayan.apps.documents.icons.icon_document_page_disable',
    kwargs={'pk': 'resolved_object.id'},
    permissions=(permission_document_edit,), text=_('Disable page'),
    view='documents:document_page_disable'
)
link_document_page_multiple_disable = Link(
    icon_class_path='mayan.apps.documents.icons.icon_document_page_disable',
    text=_('Disable pages'),
    view='documents:document_page_multiple_disable'
)
link_document_page_enable = Link(
    condition=is_document_page_disabled,
    icon_class_path='mayan.apps.documents.icons.icon_document_page_enable',
    kwargs={'pk': 'resolved_object.id'},
    permissions=(permission_document_edit,), text=_('Enable page'),
    view='documents:document_page_enable'
)
link_document_page_multiple_enable = Link(
    icon_class_path='mayan.apps.documents.icons.icon_document_page_enable',
    text=_('Enable pages'),
    view='documents:document_page_multiple_enable'
)
link_document_page_navigation_first = Link(
    args='resolved_object.pk', conditional_disable=is_first_page,
    icon_class=icon_document_page_navigation_first,
    keep_query=True, permissions=(permission_document_view,),
    text=_('First page'), view='documents:document_page_navigation_first',
)
link_document_page_navigation_last = Link(
    args='resolved_object.pk', conditional_disable=is_last_page,
    icon_class=icon_document_page_navigation_last,
    keep_query=True, text=_('Last page'),
    permissions=(permission_document_view,),
    view='documents:document_page_navigation_last',
)
link_document_page_navigation_previous = Link(
    args='resolved_object.pk', conditional_disable=is_first_page,
    icon_class=icon_document_page_navigation_previous,
    keep_query=True, permissions=(permission_document_view,),
    text=_('Previous page'),
    view='documents:document_page_navigation_previous',
)
link_document_page_navigation_next = Link(
    args='resolved_object.pk', conditional_disable=is_last_page,
    icon_class=icon_document_page_navigation_next,
    keep_query=True, text=_('Next page'),
    permissions=(permission_document_view,),
    view='documents:document_page_navigation_next',
)
link_document_page_return = Link(
    args='resolved_object.document.pk', icon_class=icon_document_page_return,
    permissions=(permission_document_view,), text=_('Document'),
    view='documents:document_preview',
)
link_document_page_rotate_left = Link(
    args='resolved_object.pk', icon_class=icon_document_page_rotate_left,
    keep_query=True, permissions=(permission_document_view,),
    text=_('Rotate left'), view='documents:document_page_rotate_left',
)
link_document_page_rotate_right = Link(
    args='resolved_object.pk', icon_class=icon_document_page_rotate_right,
    keep_query=True, permissions=(permission_document_view,),
    text=_('Rotate right'), view='documents:document_page_rotate_right',
)
link_document_page_view = Link(
    conditional_disable=is_document_page_disabled,
    icon_class_path='mayan.apps.documents.icons.icon_document_page_view',
    permissions=(permission_document_view,), text=_('Page image'),
    view='documents:document_page_view', args='resolved_object.pk'
)
link_document_page_view_reset = Link(
    icon_class_path='mayan.apps.documents.icons.icon_document_page_view_reset',
    permissions=(permission_document_view,), text=_('Reset view'),
    view='documents:document_page_view_reset', args='resolved_object.pk'
)
link_document_page_zoom_in = Link(
    args='resolved_object.pk', conditional_disable=is_max_zoom,
    icon_class=icon_document_page_zoom_in, keep_query=True,
    permissions=(permission_document_view,), text=_('Zoom in'),
    view='documents:document_page_zoom_in',
)
link_document_page_zoom_out = Link(
    args='resolved_object.pk', conditional_disable=is_min_zoom,
    icon_class=icon_document_page_zoom_out, keep_query=True,
    permissions=(permission_document_view,), text=_('Zoom out'),
    view='documents:document_page_zoom_out',
)
link_document_pages = Link(
    args='resolved_object.pk',
    icon_class_path='mayan.apps.documents.icons.icon_document_pages',
    permissions=(permission_document_view,), text=_('Pages'),
    view='documents:document_pages',
)
link_document_multiple_update_page_count = Link(
    icon_class_path='mayan.apps.documents.icons.icon_document_page_count_update',
    text=_('Recalculate page count'),
    view='documents:document_multiple_update_page_count'
)
link_document_update_page_count = Link(
    args='resolved_object.pk',
    icon_class_path='mayan.apps.documents.icons.icon_document_page_count_update',
    permissions=(permission_document_tools,),
    text=_('Recalculate page count'),
    view='documents:document_update_page_count'
)
