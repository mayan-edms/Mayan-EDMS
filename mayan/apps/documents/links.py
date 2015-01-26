from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from events.permissions import PERMISSION_EVENTS_VIEW

from .permissions import (
    PERMISSION_DOCUMENT_PROPERTIES_EDIT, PERMISSION_DOCUMENT_VIEW,
    PERMISSION_DOCUMENT_DELETE, PERMISSION_DOCUMENT_DOWNLOAD,
    PERMISSION_DOCUMENT_TRANSFORM, PERMISSION_DOCUMENT_TOOLS,
    PERMISSION_DOCUMENT_EDIT, PERMISSION_DOCUMENT_VERSION_REVERT,
    PERMISSION_DOCUMENT_TYPE_EDIT, PERMISSION_DOCUMENT_TYPE_DELETE,
    PERMISSION_DOCUMENT_TYPE_CREATE, PERMISSION_DOCUMENT_TYPE_VIEW
)
from .settings import ZOOM_MAX_LEVEL, ZOOM_MIN_LEVEL

# Document page links expressions


def is_first_page(context):
    return context['page'].page_number <= 1


def is_last_page(context):
    return context['page'].page_number >= context['page'].document_version.pages.count()


def is_min_zoom(context):
    return context['zoom'] <= ZOOM_MIN_LEVEL


def is_max_zoom(context):
    return context['zoom'] >= ZOOM_MAX_LEVEL


def is_current_version(context):
    return context['object'].document.latest_version.timestamp == context['object'].timestamp


document_list = {'text': _('All documents'), 'view': 'documents:document_list', 'famfam': 'page', 'icon': 'main/icons/page.png'}
document_list_recent = {'text': _('Recent documents'), 'view': 'documents:document_list_recent', 'famfam': 'page', 'icon': 'main/icons/page.png'}
document_preview = {'text': _('Preview'), 'view': 'documents:document_preview', 'args': 'object.id', 'famfam': 'page', 'permissions': [PERMISSION_DOCUMENT_VIEW]}
document_content = {'text': _('Content'), 'view': 'documents:document_content', 'args': 'object.id', 'famfam': 'page_white_text', 'permissions': [PERMISSION_DOCUMENT_VIEW]}
document_properties = {'text': _('Properties'), 'view': 'documents:document_properties', 'args': 'object.id', 'famfam': 'page_gear', 'permissions': [PERMISSION_DOCUMENT_VIEW]}
document_delete = {'text': _('Delete'), 'view': 'documents:document_delete', 'args': 'object.id', 'famfam': 'page_delete', 'permissions': [PERMISSION_DOCUMENT_DELETE]}
document_multiple_delete = {'text': _('Delete'), 'view': 'documents:document_multiple_delete', 'famfam': 'page_delete', 'permissions': [PERMISSION_DOCUMENT_DELETE]}
document_edit = {'text': _('Edit properties'), 'view': 'documents:document_edit', 'args': 'object.id', 'famfam': 'page_edit', 'permissions': [PERMISSION_DOCUMENT_PROPERTIES_EDIT]}
document_document_type_edit = {'text': _('Change type'), 'view': 'documents:document_document_type_edit', 'args': 'object.id', 'famfam': 'layout', 'permissions': [PERMISSION_DOCUMENT_PROPERTIES_EDIT]}
document_multiple_document_type_edit = {'text': _('Change type'), 'view': 'documents:document_multiple_document_type_edit', 'famfam': 'layout', 'permissions': [PERMISSION_DOCUMENT_PROPERTIES_EDIT]}
document_download = {'text': _('Download'), 'view': 'documents:document_download', 'args': 'object.id', 'famfam': 'page_save', 'permissions': [PERMISSION_DOCUMENT_DOWNLOAD]}
document_multiple_download = {'text': _('Download'), 'view': 'documents:document_multiple_download', 'famfam': 'page_save', 'permissions': [PERMISSION_DOCUMENT_DOWNLOAD]}
document_version_download = {'text': _('Download'), 'view': 'documents:document_version_download', 'args': 'object.pk', 'famfam': 'page_save', 'permissions': [PERMISSION_DOCUMENT_DOWNLOAD]}
document_update_page_count = {'text': _('Reset page count'), 'view': 'documents:document_update_page_count', 'args': 'object.pk', 'famfam': 'page_white_csharp', 'permissions': [PERMISSION_DOCUMENT_TOOLS]}
document_multiple_update_page_count = {'text': _('Reset page count'), 'view': 'documents:document_multiple_update_page_count', 'famfam': 'page_white_csharp', 'permissions': [PERMISSION_DOCUMENT_TOOLS]}
document_clear_transformations = {'text': _('Clear transformations'), 'view': 'documents:document_clear_transformations', 'args': 'object.id', 'famfam': 'page_paintbrush', 'permissions': [PERMISSION_DOCUMENT_TRANSFORM]}
document_multiple_clear_transformations = {'text': _('Clear transformations'), 'view': 'documents:document_multiple_clear_transformations', 'famfam': 'page_paintbrush', 'permissions': [PERMISSION_DOCUMENT_TRANSFORM]}
document_print = {'text': _('Print'), 'view': 'documents:document_print', 'args': 'object.id', 'famfam': 'printer', 'permissions': [PERMISSION_DOCUMENT_VIEW]}
document_events_view = {'text': _('Events'), 'view': 'events:events_for_object', 'args': ['"documents"', '"document"', 'object.id'], 'famfam': 'book_go', 'permissions': [PERMISSION_EVENTS_VIEW]}

# Tools
document_clear_image_cache = {'text': _('Clear the document image cache'), 'view': 'documents:document_clear_image_cache', 'famfam': 'camera_delete', 'permissions': [PERMISSION_DOCUMENT_TOOLS], 'description': _('Clear the graphics representations used to speed up the documents\' display and interactive transformations results.')}

# Document pages
document_page_transformation_list = {'text': _('Page transformations'), 'class': 'no-parent-history', 'view': 'documents:document_page_transformation_list', 'args': 'page.pk', 'famfam': 'pencil_go', 'permissions': [PERMISSION_DOCUMENT_TRANSFORM]}
document_page_transformation_create = {'text': _('Create new transformation'), 'class': 'no-parent-history', 'view': 'documents:document_page_transformation_create', 'args': 'page.pk', 'famfam': 'pencil_add', 'permissions': [PERMISSION_DOCUMENT_TRANSFORM]}
document_page_transformation_edit = {'text': _('Edit'), 'class': 'no-parent-history', 'view': 'documents:document_page_transformation_edit', 'args': 'transformation.pk', 'famfam': 'pencil_go', 'permissions': [PERMISSION_DOCUMENT_TRANSFORM]}
document_page_transformation_delete = {'text': _('Delete'), 'class': 'no-parent-history', 'view': 'documents:document_page_transformation_delete', 'args': 'transformation.pk', 'famfam': 'pencil_delete', 'permissions': [PERMISSION_DOCUMENT_TRANSFORM]}

document_page_view = {'text': _('Page image'), 'class': 'no-parent-history', 'view': 'documents:document_page_view', 'args': 'page.pk', 'famfam': 'page_white_picture', 'permissions': [PERMISSION_DOCUMENT_VIEW]}
document_page_text = {'text': _('Page text'), 'class': 'no-parent-history', 'view': 'documents:document_page_text', 'args': 'page.pk', 'famfam': 'page_white_text', 'permissions': [PERMISSION_DOCUMENT_VIEW]}
document_page_edit = {'text': _('Edit page text'), 'class': 'no-parent-history', 'view': 'documents:document_page_edit', 'args': 'page.pk', 'famfam': 'page_white_edit', 'permissions': [PERMISSION_DOCUMENT_EDIT]}
document_page_navigation_next = {'text': _('Next page'), 'class': 'no-parent-history', 'view': 'documents:document_page_navigation_next', 'args': 'page.pk', 'famfam': 'resultset_next', 'permissions': [PERMISSION_DOCUMENT_VIEW], 'conditional_disable': is_last_page, 'keep_query': True}
document_page_navigation_previous = {'text': _('Previous page'), 'class': 'no-parent-history', 'view': 'documents:document_page_navigation_previous', 'args': 'page.pk', 'famfam': 'resultset_previous', 'permissions': [PERMISSION_DOCUMENT_VIEW], 'conditional_disable': is_first_page, 'keep_query': True}
document_page_navigation_first = {'text': _('First page'), 'class': 'no-parent-history', 'view': 'documents:document_page_navigation_first', 'args': 'page.pk', 'famfam': 'resultset_first', 'permissions': [PERMISSION_DOCUMENT_VIEW], 'conditional_disable': is_first_page, 'keep_query': True}
document_page_navigation_last = {'text': _('Last page'), 'class': 'no-parent-history', 'view': 'documents:document_page_navigation_last', 'args': 'page.pk', 'famfam': 'resultset_last', 'permissions': [PERMISSION_DOCUMENT_VIEW], 'conditional_disable': is_last_page, 'keep_query': True}
document_page_zoom_in = {'text': _('Zoom in'), 'class': 'no-parent-history', 'view': 'documents:document_page_zoom_in', 'args': 'page.pk', 'famfam': 'zoom_in', 'permissions': [PERMISSION_DOCUMENT_VIEW], 'conditional_disable': is_max_zoom}
document_page_zoom_out = {'text': _('Zoom out'), 'class': 'no-parent-history', 'view': 'documents:document_page_zoom_out', 'args': 'page.pk', 'famfam': 'zoom_out', 'permissions': [PERMISSION_DOCUMENT_VIEW], 'conditional_disable': is_min_zoom}
document_page_rotate_right = {'text': _('Rotate right'), 'class': 'no-parent-history', 'view': 'documents:document_page_rotate_right', 'args': 'page.pk', 'famfam': 'arrow_turn_right', 'permissions': [PERMISSION_DOCUMENT_VIEW]}
document_page_rotate_left = {'text': _('Rotate left'), 'class': 'no-parent-history', 'view': 'documents:document_page_rotate_left', 'args': 'page.pk', 'famfam': 'arrow_turn_left', 'permissions': [PERMISSION_DOCUMENT_VIEW]}
document_page_view_reset = {'text': _('Reset view'), 'class': 'no-parent-history', 'view': 'documents:document_page_view_reset', 'args': 'page.pk', 'famfam': 'page_white', 'permissions': [PERMISSION_DOCUMENT_VIEW]}

# Document versions
document_version_list = {'text': _('Versions'), 'view': 'documents:document_version_list', 'args': 'object.pk', 'famfam': 'page_world', 'permissions': [PERMISSION_DOCUMENT_VIEW]}
document_version_revert = {'text': _('Revert'), 'view': 'documents:document_version_revert', 'args': 'object.pk', 'famfam': 'page_refresh', 'permissions': [PERMISSION_DOCUMENT_VERSION_REVERT], 'conditional_disable': is_current_version}

# Document type related links
document_type_list = {'text': _('Document types'), 'view': 'documents:document_type_list', 'famfam': 'layout', 'permissions': [PERMISSION_DOCUMENT_TYPE_VIEW]}
document_type_setup = {'text': _('Document types'), 'view': 'documents:document_type_list', 'famfam': 'layout', 'icon': 'main/icons/layout.png', 'permissions': [PERMISSION_DOCUMENT_TYPE_VIEW]}
document_type_edit = {'text': _('Edit'), 'view': 'documents:document_type_edit', 'args': 'document_type.id', 'famfam': 'layout_edit', 'permissions': [PERMISSION_DOCUMENT_TYPE_EDIT]}
document_type_delete = {'text': _('Delete'), 'view': 'documents:document_type_delete', 'args': 'document_type.id', 'famfam': 'layout_delete', 'permissions': [PERMISSION_DOCUMENT_TYPE_DELETE]}
document_type_create = {'text': _('Create document type'), 'view': 'documents:document_type_create', 'famfam': 'layout_add', 'permissions': [PERMISSION_DOCUMENT_TYPE_CREATE]}

document_type_filename_list = {'text': _('Filenames'), 'view': 'documents:document_type_filename_list', 'args': 'document_type.id', 'famfam': 'database', 'permissions': [PERMISSION_DOCUMENT_TYPE_VIEW]}
document_type_filename_create = {'text': _('Add filename to document type'), 'view': 'documents:document_type_filename_create', 'args': 'document_type.id', 'famfam': 'database_add', 'permissions': [PERMISSION_DOCUMENT_TYPE_EDIT]}
document_type_filename_edit = {'text': _('Edit'), 'view': 'documents:document_type_filename_edit', 'args': 'filename.id', 'famfam': 'database_edit', 'permissions': [PERMISSION_DOCUMENT_TYPE_EDIT]}
document_type_filename_delete = {'text': _('Delete'), 'view': 'documents:document_type_filename_delete', 'args': 'filename.id', 'famfam': 'database_delete', 'permissions': [PERMISSION_DOCUMENT_TYPE_EDIT]}
