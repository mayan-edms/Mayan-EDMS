from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from converter.permissions import (
    permission_transformation_delete, permission_transformation_edit
)
from navigation import Link

from .icons import (
    icon_clear_image_cache, icon_document_duplicates_list, icon_document_list,
    icon_document_list_deleted, icon_document_list_favorites,
    icon_document_list_recent_access, icon_document_list_recent_added,
    icon_document_page_navigation_first, icon_document_page_navigation_last,
    icon_document_page_navigation_next, icon_document_page_navigation_previous,
    icon_document_page_return, icon_document_page_rotate_left,
    icon_document_page_rotate_right, icon_document_page_zoom_in,
    icon_document_page_zoom_out, icon_document_pages, icon_document_preview,
    icon_document_properties, icon_document_type_create,
    icon_document_type_delete, icon_document_type_edit,
    icon_document_type_filename_create, icon_document_type_setup,
    icon_document_version_list, icon_document_version_return_document,
    icon_document_version_return_list, icon_duplicated_document_list,
    icon_duplicated_document_scan
)
from .permissions import (
    permission_document_delete, permission_document_download,
    permission_document_properties_edit, permission_document_print,
    permission_document_restore, permission_document_tools,
    permission_document_version_revert, permission_document_view,
    permission_document_trash, permission_document_type_create,
    permission_document_type_delete, permission_document_type_edit,
    permission_document_type_view, permission_empty_trash,
    permission_document_version_view
)
from .settings import setting_zoom_max_level, setting_zoom_min_level


def is_not_current_version(context):
    # Use the 'object' key when the document version is an object in a list,
    # such as when showing the version list view and use the 'resolved_object'
    # when the document version is the context object, such as when showing the
    # signatures list of a documern version. This can be fixed by updating
    # the navigations app object resolution logic to use 'resolved_object' even
    # for objects in a list.
    document_version = context.get('object', context['resolved_object'])
    return document_version.document.latest_version.timestamp != document_version.timestamp


def is_first_page(context):
    return context['resolved_object'].page_number <= 1


def is_last_page(context):
    return context['resolved_object'].page_number >= context['resolved_object'].document_version.pages.count()


def is_max_zoom(context):
    return context['zoom'] >= setting_zoom_max_level.value


def is_min_zoom(context):
    return context['zoom'] <= setting_zoom_min_level.value


# Facet
link_document_preview = Link(
    args='resolved_object.id', icon_class=icon_document_preview,
    permissions=(permission_document_view,),
    text=_('Preview'), view='documents:document_preview',
)
link_document_properties = Link(
    args='resolved_object.id', icon_class=icon_document_properties,
    permissions=(permission_document_view,),
    text=_('Properties'), view='documents:document_properties',
)
link_document_version_list = Link(
    args='resolved_object.pk', icon_class=icon_document_version_list,
    permissions=(permission_document_version_view,),
    text=_('Versions'), view='documents:document_version_list',
)
link_document_pages = Link(
    args='resolved_object.pk', icon_class=icon_document_pages,
    permissions=(permission_document_view,), text=_('Pages'),
    view='documents:document_pages',
)

# Actions
link_document_clear_transformations = Link(
    args='resolved_object.id',
    permissions=(permission_transformation_delete,),
    text=_('Clear transformations'),
    view='documents:document_clear_transformations',
)
link_document_clone_transformations = Link(
    args='resolved_object.id', permissions=(permission_transformation_edit,),
    text=_('Clone transformations'),
    view='documents:document_clone_transformations',
)
link_document_delete = Link(
    args='resolved_object.id', permissions=(permission_document_delete,),
    tags='dangerous', text=_('Delete'), view='documents:document_delete',
)
link_document_favorites_add = Link(
    args='resolved_object.id',
    permissions=(permission_document_view,), text=_('Add to favorites'),
    view='documents:document_add_to_favorites',
)
link_document_favorites_remove = Link(
    args='resolved_object.id',
    permissions=(permission_document_view,), text=_('Remove from favorites'),
    view='documents:document_remove_from_favorites',
)
link_document_trash = Link(
    args='resolved_object.id', permissions=(permission_document_trash,),
    tags='dangerous', text=_('Move to trash'),
    view='documents:document_trash',
)
link_document_edit = Link(
    args='resolved_object.id',
    permissions=(permission_document_properties_edit,),
    text=_('Edit properties'), view='documents:document_edit',
)
link_document_document_type_edit = Link(
    args='resolved_object.id',
    permissions=(permission_document_properties_edit,), text=_('Change type'),
    view='documents:document_document_type_edit',
)
link_document_download = Link(
    args='resolved_object.id', permissions=(permission_document_download,),
    text=_('Advanced download'), view='documents:document_download_form',
)
link_document_print = Link(
    args='resolved_object.id', permissions=(permission_document_print,),
    text=_('Print'), view='documents:document_print',
)
link_document_quick_download = Link(
    args='resolved_object.id', permissions=(permission_document_download,),
    text=_('Quick download'), view='documents:document_download',
)
link_document_update_page_count = Link(
    args='resolved_object.pk', permissions=(permission_document_tools,),
    text=_('Recalculate page count'),
    view='documents:document_update_page_count'
)
link_document_restore = Link(
    permissions=(permission_document_restore,), text=_('Restore'),
    view='documents:document_restore', args='object.pk'
)
link_document_multiple_clear_transformations = Link(
    permissions=(permission_transformation_delete,),
    text=_('Clear transformations'),
    view='documents:document_multiple_clear_transformations'
)
link_document_multiple_trash = Link(
    tags='dangerous', text=_('Move to trash'),
    view='documents:document_multiple_trash'
)
link_document_multiple_delete = Link(
    tags='dangerous', text=_('Delete'),
    view='documents:document_multiple_delete'
)
link_document_multiple_favorites_add = Link(
    text=_('Add to favorites'),
    view='documents:document_multiple_add_to_favorites',
)
link_document_multiple_favorites_remove = Link(
    text=_('Remove from favorites'),
    view='documents:document_multiple_remove_from_favorites',
)
link_document_multiple_document_type_edit = Link(
    text=_('Change type'),
    view='documents:document_multiple_document_type_edit'
)
link_document_multiple_download = Link(
    text=_('Advanced download'), view='documents:document_multiple_download_form'
)
link_document_multiple_update_page_count = Link(
    text=_('Recalculate page count'),
    view='documents:document_multiple_update_page_count'
)
link_document_multiple_restore = Link(
    text=_('Restore'), view='documents:document_multiple_restore'
)

# Versions
link_document_version_download = Link(
    args='resolved_object.pk', permissions=(permission_document_download,),
    text=_('Download version'), view='documents:document_version_download_form'
)
link_document_version_return_document = Link(
    args='resolved_object.document.pk',
    icon_class=icon_document_version_return_document,
    permissions=(permission_document_view,), text=_('Document'),
    view='documents:document_preview',
)
link_document_version_return_list = Link(
    args='resolved_object.document.pk',
    icon_class=icon_document_version_return_list,
    permissions=(permission_document_version_view,), text=_('Versions'),
    view='documents:document_version_list',
)
link_document_version_view = Link(
    args='resolved_object.pk', permissions=(permission_document_version_view,),
    text=_('Details'), view='documents:document_version_view'
)

# Views
link_document_list = Link(
    icon_class=icon_document_list, text=_('All documents'),
    view='documents:document_list'
)
link_document_list_favorites = Link(
    icon_class=icon_document_list_favorites, text=_('Favorites'),
    view='documents:document_list_favorites'
)
link_document_list_recent_access = Link(
    icon_class=icon_document_list_recent_access, text=_('Recently accessed'),
    view='documents:document_list_recent_access'
)
link_document_list_recent_added = Link(
    icon_class=icon_document_list_recent_added, text=_('Recently added'),
    view='documents:document_list_recent_added'
)
link_document_list_deleted = Link(
    icon_class=icon_document_list_deleted, text=_('Trash can'),
    view='documents:document_list_deleted'
)

# Tools
link_clear_image_cache = Link(
    icon_class=icon_clear_image_cache,
    description=_(
        'Clear the graphics representations used to speed up the documents\' '
        'display and interactive transformations results.'
    ), permissions=(permission_document_tools,),
    text=_('Clear document image cache'),
    view='documents:document_clear_image_cache'
)
link_trash_can_empty = Link(
    permissions=(permission_empty_trash,), text=_('Empty trash'),
    view='documents:trash_can_empty'
)

# Document pages
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
    permissions=(permission_document_view,), text=_('Page image'),
    view='documents:document_page_view', args='resolved_object.pk'
)
link_document_page_view_reset = Link(
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

# Document versions
link_document_version_revert = Link(
    args='object.pk', condition=is_not_current_version,
    permissions=(permission_document_version_revert,), tags='dangerous',
    text=_('Revert'), view='documents:document_version_revert',
)

# Document type related links
link_document_type_create = Link(
    icon_class=icon_document_type_create,
    permissions=(permission_document_type_create,),
    text=_('Create document type'), view='documents:document_type_create'
)
link_document_type_delete = Link(
    args='resolved_object.id', icon_class=icon_document_type_delete,
    permissions=(permission_document_type_delete,), tags='dangerous',
    text=_('Delete'), view='documents:document_type_delete',
)
link_document_type_edit = Link(
    args='resolved_object.id', icon_class=icon_document_type_edit,
    permissions=(permission_document_type_edit,), text=_('Edit'),
    view='documents:document_type_edit',
)
link_document_type_filename_create = Link(
    args='document_type.id', icon_class=icon_document_type_filename_create,
    permissions=(permission_document_type_edit,),
    text=_('Add quick label to document type'),
    view='documents:document_type_filename_create',
)
link_document_type_filename_delete = Link(
    args='resolved_object.id', permissions=(permission_document_type_edit,),
    tags='dangerous', text=_('Delete'),
    view='documents:document_type_filename_delete',
)
link_document_type_filename_edit = Link(
    args='resolved_object.id', permissions=(permission_document_type_edit,),
    text=_('Edit'), view='documents:document_type_filename_edit',
)
link_document_type_filename_list = Link(
    args='resolved_object.id', permissions=(permission_document_type_view,),
    text=_('Quick labels'), view='documents:document_type_filename_list',
)
link_document_type_list = Link(
    permissions=(permission_document_type_view,), text=_('Document types'),
    view='documents:document_type_list'
)
link_document_type_setup = Link(
    icon_class=icon_document_type_setup,
    permissions=(permission_document_type_view,), text=_('Document types'),
    view='documents:document_type_list'
)
link_duplicated_document_list = Link(
    icon_class=icon_duplicated_document_list, text=_('Duplicated documents'),
    view='documents:duplicated_document_list'
)
link_document_duplicates_list = Link(
    args='resolved_object.id', icon_class=icon_document_duplicates_list,
    permissions=(permission_document_view,), text=_('Duplicates'),
    view='documents:document_duplicates_list',
)
link_duplicated_document_scan = Link(
    icon_class=icon_duplicated_document_scan,
    permissions=(permission_document_tools,),
    text=_('Duplicated document scan'),
    view='documents:duplicated_document_scan'
)
