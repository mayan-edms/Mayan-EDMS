from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from history.permissions import PERMISSION_HISTORY_VIEW

from .conf.settings import ZOOM_MAX_LEVEL, ZOOM_MIN_LEVEL
from .permissions import (PERMISSION_DOCUMENT_PROPERTIES_EDIT,
                          PERMISSION_DOCUMENT_VIEW, PERMISSION_DOCUMENT_DELETE,
                          PERMISSION_DOCUMENT_DOWNLOAD, PERMISSION_DOCUMENT_TRANSFORM,
                          PERMISSION_DOCUMENT_TOOLS, PERMISSION_DOCUMENT_EDIT,
                          PERMISSION_DOCUMENT_VERSION_REVERT, PERMISSION_DOCUMENT_TYPE_EDIT,
                          PERMISSION_DOCUMENT_TYPE_DELETE, PERMISSION_DOCUMENT_TYPE_CREATE,
                          PERMISSION_DOCUMENT_TYPE_VIEW)

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


document_list = {'text': _(u'all documents'), 'view': 'document_list', 'famfam': 'page'}
document_list_recent = {'text': _(u'recent documents'), 'view': 'document_list_recent', 'famfam': 'page'}
document_view_simple = {'text': _(u'details'), 'view': 'document_view_simple', 'args': 'object.id', 'famfam': 'page', 'permissions': [PERMISSION_DOCUMENT_VIEW]}
document_view_advanced = {'text': _(u'properties'), 'view': 'document_view_advanced', 'args': 'object.id', 'famfam': 'page_gear', 'permissions': [PERMISSION_DOCUMENT_VIEW]}
document_delete = {'text': _(u'delete'), 'view': 'document_delete', 'args': 'object.id', 'famfam': 'page_delete', 'permissions': [PERMISSION_DOCUMENT_DELETE]}
document_multiple_delete = {'text': _(u'delete'), 'view': 'document_multiple_delete', 'famfam': 'page_delete', 'permissions': [PERMISSION_DOCUMENT_DELETE]}
document_edit = {'text': _(u'edit'), 'view': 'document_edit', 'args': 'object.id', 'famfam': 'page_edit', 'permissions': [PERMISSION_DOCUMENT_PROPERTIES_EDIT]}
document_download = {'text': _(u'download'), 'view': 'document_download', 'args': 'object.id', 'famfam': 'page_save', 'permissions': [PERMISSION_DOCUMENT_DOWNLOAD]}
document_multiple_download = {'text': _(u'download'), 'view': 'document_multiple_download', 'famfam': 'page_save', 'permissions': [PERMISSION_DOCUMENT_DOWNLOAD]}
document_version_download = {'text': _(u'download'), 'view': 'document_version_download', 'args': 'object.pk', 'famfam': 'page_save', 'permissions': [PERMISSION_DOCUMENT_DOWNLOAD]}
document_find_duplicates = {'text': _(u'find duplicates'), 'view': 'document_find_duplicates', 'args': 'object.id', 'famfam': 'page_white_copy', 'permissions': [PERMISSION_DOCUMENT_VIEW]}
document_find_all_duplicates = {'text': _(u'find all duplicates'), 'view': 'document_find_all_duplicates', 'famfam': 'page_white_copy', 'permissions': [PERMISSION_DOCUMENT_VIEW], 'description': _(u'Search all the documents\' checksums and return a list of the exact matches.')}
document_update_page_count = {'text': _(u'update office documents\' page count'), 'view': 'document_update_page_count', 'famfam': 'page_white_csharp', 'permissions': [PERMISSION_DOCUMENT_TOOLS], 'description': _(u'Update the page count of the office type documents.  This is useful when enabling office document support after there were already office type documents in the database.')}
document_clear_transformations = {'text': _(u'clear transformations'), 'view': 'document_clear_transformations', 'args': 'object.id', 'famfam': 'page_paintbrush', 'permissions': [PERMISSION_DOCUMENT_TRANSFORM]}
document_multiple_clear_transformations = {'text': _(u'clear transformations'), 'view': 'document_multiple_clear_transformations', 'famfam': 'page_paintbrush', 'permissions': [PERMISSION_DOCUMENT_TRANSFORM]}
document_print = {'text': _(u'print'), 'view': 'document_print', 'args': 'object.id', 'famfam': 'printer', 'permissions': [PERMISSION_DOCUMENT_VIEW]}
document_history_view = {'text': _(u'history'), 'view': 'history_for_object', 'args': ['"documents"', '"document"', 'object.id'], 'famfam': 'book_go', 'permissions': [PERMISSION_HISTORY_VIEW]}
document_missing_list = {'text': _(u'Find missing document files'), 'view': 'document_missing_list', 'famfam': 'folder_page', 'permissions': [PERMISSION_DOCUMENT_VIEW]}

# Tools
document_clear_image_cache = {'text': _(u'Clear the document image cache'), 'view': 'document_clear_image_cache', 'famfam': 'camera_delete', 'permissions': [PERMISSION_DOCUMENT_TOOLS], 'description': _(u'Clear the graphics representations used to speed up the documents\' display and interactive transformations results.')}

# Document pages
document_page_transformation_list = {'text': _(u'page transformations'), 'class': 'no-parent-history', 'view': 'document_page_transformation_list', 'args': 'page.pk', 'famfam': 'pencil_go', 'permissions': [PERMISSION_DOCUMENT_TRANSFORM]}
document_page_transformation_create = {'text': _(u'create new transformation'), 'class': 'no-parent-history', 'view': 'document_page_transformation_create', 'args': 'page.pk', 'famfam': 'pencil_add', 'permissions': [PERMISSION_DOCUMENT_TRANSFORM]}
document_page_transformation_edit = {'text': _(u'edit'), 'class': 'no-parent-history', 'view': 'document_page_transformation_edit', 'args': 'transformation.pk', 'famfam': 'pencil_go', 'permissions': [PERMISSION_DOCUMENT_TRANSFORM]}
document_page_transformation_delete = {'text': _(u'delete'), 'class': 'no-parent-history', 'view': 'document_page_transformation_delete', 'args': 'transformation.pk', 'famfam': 'pencil_delete', 'permissions': [PERMISSION_DOCUMENT_TRANSFORM]}

document_page_view = {'text': _(u'page image'), 'class': 'no-parent-history', 'view': 'document_page_view', 'args': 'page.pk', 'famfam': 'page_white_picture', 'permissions': [PERMISSION_DOCUMENT_VIEW]}
document_page_text = {'text': _(u'page text'), 'class': 'no-parent-history', 'view': 'document_page_text', 'args': 'page.pk', 'famfam': 'page_white_text', 'permissions': [PERMISSION_DOCUMENT_VIEW]}
document_page_edit = {'text': _(u'edit page text'), 'class': 'no-parent-history', 'view': 'document_page_edit', 'args': 'page.pk', 'famfam': 'page_white_edit', 'permissions': [PERMISSION_DOCUMENT_EDIT]}
document_page_navigation_next = {'text': _(u'next page'), 'class': 'no-parent-history', 'view': 'document_page_navigation_next', 'args': 'page.pk', 'famfam': 'resultset_next', 'permissions': [PERMISSION_DOCUMENT_VIEW], 'conditional_disable': is_last_page}
document_page_navigation_previous = {'text': _(u'previous page'), 'class': 'no-parent-history', 'view': 'document_page_navigation_previous', 'args': 'page.pk', 'famfam': 'resultset_previous', 'permissions': [PERMISSION_DOCUMENT_VIEW], 'conditional_disable': is_first_page}
document_page_navigation_first = {'text': _(u'first page'), 'class': 'no-parent-history', 'view': 'document_page_navigation_first', 'args': 'page.pk', 'famfam': 'resultset_first', 'permissions': [PERMISSION_DOCUMENT_VIEW], 'conditional_disable': is_first_page}
document_page_navigation_last = {'text': _(u'last page'), 'class': 'no-parent-history', 'view': 'document_page_navigation_last', 'args': 'page.pk', 'famfam': 'resultset_last', 'permissions': [PERMISSION_DOCUMENT_VIEW], 'conditional_disable': is_last_page}
document_page_zoom_in = {'text': _(u'zoom in'), 'class': 'no-parent-history', 'view': 'document_page_zoom_in', 'args': 'page.pk', 'famfam': 'zoom_in', 'permissions': [PERMISSION_DOCUMENT_VIEW], 'conditional_disable': is_max_zoom}
document_page_zoom_out = {'text': _(u'zoom out'), 'class': 'no-parent-history', 'view': 'document_page_zoom_out', 'args': 'page.pk', 'famfam': 'zoom_out', 'permissions': [PERMISSION_DOCUMENT_VIEW], 'conditional_disable': is_min_zoom}
document_page_rotate_right = {'text': _(u'rotate right'), 'class': 'no-parent-history', 'view': 'document_page_rotate_right', 'args': 'page.pk', 'famfam': 'arrow_turn_right', 'permissions': [PERMISSION_DOCUMENT_VIEW]}
document_page_rotate_left = {'text': _(u'rotate left'), 'class': 'no-parent-history', 'view': 'document_page_rotate_left', 'args': 'page.pk', 'famfam': 'arrow_turn_left', 'permissions': [PERMISSION_DOCUMENT_VIEW]}
document_page_view_reset = {'text': _(u'reset view'), 'class': 'no-parent-history', 'view': 'document_page_view_reset', 'args': 'page.pk', 'famfam': 'page_white', 'permissions': [PERMISSION_DOCUMENT_VIEW]}

# Document versions
document_version_list = {'text': _(u'versions'), 'view': 'document_version_list', 'args': 'object.pk', 'famfam': 'page_world', 'permissions': [PERMISSION_DOCUMENT_VIEW]}
document_version_revert = {'text': _(u'revert'), 'view': 'document_version_revert', 'args': 'object.pk', 'famfam': 'page_refresh', 'permissions': [PERMISSION_DOCUMENT_VERSION_REVERT], 'conditional_disable': is_current_version}

# Document type related links
document_type_list = {'text': _(u'document type list'), 'view': 'document_type_list', 'famfam': 'layout', 'permissions': [PERMISSION_DOCUMENT_TYPE_VIEW]}
document_type_setup = {'text': _(u'document types'), 'view': 'document_type_list', 'famfam': 'layout', 'icon': 'layout.png', 'permissions': [PERMISSION_DOCUMENT_TYPE_VIEW], 'children_view_regex': [r'^document_type_']}
document_type_edit = {'text': _(u'edit'), 'view': 'document_type_edit', 'args': 'document_type.id', 'famfam': 'layout_edit', 'permissions': [PERMISSION_DOCUMENT_TYPE_EDIT]}
document_type_delete = {'text': _(u'delete'), 'view': 'document_type_delete', 'args': 'document_type.id', 'famfam': 'layout_delete', 'permissions': [PERMISSION_DOCUMENT_TYPE_DELETE]}
document_type_create = {'text': _(u'create document type'), 'view': 'document_type_create', 'famfam': 'layout_add', 'permissions': [PERMISSION_DOCUMENT_TYPE_CREATE]}

document_type_filename_list = {'text': _(u'filenames'), 'view': 'document_type_filename_list', 'args': 'document_type.id', 'famfam': 'database', 'permissions': [PERMISSION_DOCUMENT_TYPE_VIEW]}
document_type_filename_create = {'text': _(u'add filename to document type'), 'view': 'document_type_filename_create', 'args': 'document_type.id', 'famfam': 'database_add', 'permissions': [PERMISSION_DOCUMENT_TYPE_EDIT]}
document_type_filename_edit = {'text': _(u'edit'), 'view': 'document_type_filename_edit', 'args': 'filename.id', 'famfam': 'database_edit', 'permissions': [PERMISSION_DOCUMENT_TYPE_EDIT]}
document_type_filename_delete = {'text': _(u'delete'), 'view': 'document_type_filename_delete', 'args': 'filename.id', 'famfam': 'database_delete', 'permissions': [PERMISSION_DOCUMENT_TYPE_EDIT]}
