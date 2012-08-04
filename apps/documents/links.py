from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation.api import Link
from history.permissions import PERMISSION_HISTORY_VIEW

from .permissions import (PERMISSION_DOCUMENT_CREATE,
    PERMISSION_DOCUMENT_PROPERTIES_EDIT, PERMISSION_DOCUMENT_VIEW,
    PERMISSION_DOCUMENT_DELETE, PERMISSION_DOCUMENT_DOWNLOAD,
    PERMISSION_DOCUMENT_TRANSFORM, PERMISSION_DOCUMENT_TOOLS,
    PERMISSION_DOCUMENT_EDIT, PERMISSION_DOCUMENT_VERSION_REVERT,
    PERMISSION_DOCUMENT_TYPE_EDIT, PERMISSION_DOCUMENT_TYPE_DELETE,
    PERMISSION_DOCUMENT_TYPE_CREATE, PERMISSION_DOCUMENT_TYPE_VIEW,
    PERMISSION_DOCUMENT_VERSIONS_TEXT_COMPARE)

from .conf.settings import ZOOM_MAX_LEVEL, ZOOM_MIN_LEVEL


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


document_list = Link(text=_(u'all documents'), view='document_list', sprite='page')
document_list_recent = Link(text=_(u'recent documents'), view='document_list_recent', sprite='page')
document_create_siblings = Link(text=_(u'clone metadata'), view='document_create_siblings', args='object.id', sprite='page_copy', permissions=[PERMISSION_DOCUMENT_CREATE])
document_view_simple = Link(text=_(u'details'), view='document_view_simple', args='object.id', sprite='page', permissions=[PERMISSION_DOCUMENT_VIEW])
document_view_advanced = Link(text=_(u'properties'), view='document_view_advanced', args='object.id', sprite='page_gear', permissions=[PERMISSION_DOCUMENT_VIEW])
document_delete = Link(text=_(u'delete'), view='document_delete', args='object.id', sprite='page_delete', permissions=[PERMISSION_DOCUMENT_DELETE])
document_multiple_delete = Link(text=_(u'delete'), view='document_multiple_delete', sprite='page_delete', permissions=[PERMISSION_DOCUMENT_DELETE])
document_edit = Link(text=_(u'edit'), view='document_edit', args='object.id', sprite='page_edit', permissions=[PERMISSION_DOCUMENT_PROPERTIES_EDIT])
document_preview = Link(text=_(u'preview'), klass='fancybox', view='document_preview', args='object.id', sprite='magnifier', permissions=[PERMISSION_DOCUMENT_VIEW])
document_download = Link(text=_(u'download'), view='document_download', args='object.id', sprite='page_save', permissions=[PERMISSION_DOCUMENT_DOWNLOAD])
document_multiple_download = Link(text=_(u'download'), view='document_multiple_download', sprite='page_save', permissions=[PERMISSION_DOCUMENT_DOWNLOAD])
document_version_download = Link(text=_(u'download'), view='document_version_download', args='object.pk', sprite='page_save', permissions=[PERMISSION_DOCUMENT_DOWNLOAD])
document_find_duplicates = Link(text=_(u'find duplicates'), view='document_find_duplicates', args='object.id', sprite='page_white_copy', permissions=[PERMISSION_DOCUMENT_VIEW])
document_find_all_duplicates = Link(text=_(u'find all duplicates'), view='document_find_all_duplicates', sprite='page_white_copy', permissions=[PERMISSION_DOCUMENT_VIEW], description=_(u'Search all the documents\' checksums and return a list of the exact matches.'))
document_update_page_count = Link(text=_(u'update office documents\' page count'), view='document_update_page_count', sprite='page_white_csharp', permissions=[PERMISSION_DOCUMENT_TOOLS], description=_(u'Update the page count of the office type documents.  This is useful when enabling office document support after there were already office type documents in the database.'))
document_clear_transformations = Link(text=_(u'clear transformations'), view='document_clear_transformations', args='object.id', sprite='page_paintbrush', permissions=[PERMISSION_DOCUMENT_TRANSFORM])
document_multiple_clear_transformations = Link(text=_(u'clear transformations'), view='document_multiple_clear_transformations', sprite='page_paintbrush', permissions=[PERMISSION_DOCUMENT_TRANSFORM])
document_print = Link(text=_(u'print'), view='document_print', args='object.id', sprite='printer', permissions=[PERMISSION_DOCUMENT_VIEW])
document_history_view = Link(text=_(u'history'), view='history_for_object', args=['"documents"', '"document"', 'object.pk'], sprite='book_go', permissions=[PERMISSION_HISTORY_VIEW])
document_missing_list = Link(text=_(u'Find missing document files'), view='document_missing_list', sprite='folder_page', permissions=[PERMISSION_DOCUMENT_VIEW])

# Tools
document_clear_image_cache = Link(text=_(u'Clear the document image cache'), view='document_clear_image_cache', sprite='camera_delete', permissions=[PERMISSION_DOCUMENT_TOOLS], description=_(u'Clear the graphics representations used to speed up the documents\' display and interactive transformations results.'))

# Document pages
document_page_transformation_list = Link(text=_(u'page transformations'), klass='no-parent-history', view='document_page_transformation_list', args='page.pk', sprite='pencil_go', permissions=[PERMISSION_DOCUMENT_TRANSFORM])
document_page_transformation_create = Link(text=_(u'create new transformation'), klass='no-parent-history', view='document_page_transformation_create', args='page.pk', sprite='pencil_add', permissions=[PERMISSION_DOCUMENT_TRANSFORM])
document_page_transformation_edit = Link(text=_(u'edit'), klass='no-parent-history', view='document_page_transformation_edit', args='transformation.pk', sprite='pencil_go', permissions=[PERMISSION_DOCUMENT_TRANSFORM])
document_page_transformation_delete = Link(text=_(u'delete'), klass='no-parent-history', view='document_page_transformation_delete', args='transformation.pk', sprite='pencil_delete', permissions=[PERMISSION_DOCUMENT_TRANSFORM])

document_page_view = Link(text=_(u'page image'), klass='no-parent-history', view='document_page_view', args='page.pk', sprite='page_white_picture', permissions=[PERMISSION_DOCUMENT_VIEW])
document_page_text = Link(text=_(u'page text'), klass='no-parent-history', view='document_page_text', args='page.pk', sprite='page_white_text', permissions=[PERMISSION_DOCUMENT_VIEW])
document_page_edit = Link(text=_(u'edit page text'), klass='no-parent-history', view='document_page_edit', args='page.pk', sprite='page_white_edit', permissions=[PERMISSION_DOCUMENT_EDIT])
document_page_navigation_next = Link(text=_(u'next page'), klass='no-parent-history', view='document_page_navigation_next', args='page.pk', sprite='resultset_next', permissions=[PERMISSION_DOCUMENT_VIEW], conditional_disable=is_last_page)
document_page_navigation_previous = Link(text=_(u'previous page'), klass='no-parent-history', view='document_page_navigation_previous', args='page.pk', sprite='resultset_previous', permissions=[PERMISSION_DOCUMENT_VIEW], conditional_disable=is_first_page)
document_page_navigation_first = Link(text=_(u'first page'), klass='no-parent-history', view='document_page_navigation_first', args='page.pk', sprite='resultset_first', permissions=[PERMISSION_DOCUMENT_VIEW], conditional_disable=is_first_page)
document_page_navigation_last = Link(text=_(u'last page'), klass='no-parent-history', view='document_page_navigation_last', args='page.pk', sprite='resultset_last', permissions=[PERMISSION_DOCUMENT_VIEW], conditional_disable=is_last_page)
document_page_zoom_in = Link(text=_(u'zoom in'), klass='no-parent-history', view='document_page_zoom_in', args='page.pk', sprite='zoom_in', permissions=[PERMISSION_DOCUMENT_VIEW], conditional_disable=is_max_zoom)
document_page_zoom_out = Link(text=_(u'zoom out'), klass='no-parent-history', view='document_page_zoom_out', args='page.pk', sprite='zoom_out', permissions=[PERMISSION_DOCUMENT_VIEW], conditional_disable=is_min_zoom)
document_page_rotate_right = Link(text=_(u'rotate right'), klass='no-parent-history', view='document_page_rotate_right', args='page.pk', sprite='arrow_turn_right', permissions=[PERMISSION_DOCUMENT_VIEW])
document_page_rotate_left = Link(text=_(u'rotate left'), klass='no-parent-history', view='document_page_rotate_left', args='page.pk', sprite='arrow_turn_left', permissions=[PERMISSION_DOCUMENT_VIEW])
document_page_view_reset = Link(text=_(u'reset view'), klass='no-parent-history', view='document_page_view_reset', args='page.pk', sprite='page_white', permissions=[PERMISSION_DOCUMENT_VIEW])

# Document versions
document_version_list = Link(text=_(u'versions'), view='document_version_list', args='object.pk', sprite='page_world', permissions=[PERMISSION_DOCUMENT_VIEW])
document_version_revert = Link(text=_(u'revert'), view='document_version_revert', args='object.pk', sprite='page_refresh', permissions=[PERMISSION_DOCUMENT_VERSION_REVERT], conditional_disable=is_current_version)
document_version_text_compare = Link(text=_(u'compare (text)'), view='document_version_text_compare', args='object.pk', sprite='table_relationship', permissions=[PERMISSION_DOCUMENT_VERSIONS_TEXT_COMPARE])

# Document type related links
document_type_list = Link(text=_(u'document type list'), view='document_type_list', sprite='layout', permissions=[PERMISSION_DOCUMENT_TYPE_VIEW])
document_type_setup = Link(text=_(u'document types'), view='document_type_list', sprite='layout', icon='layout.png', permissions=[PERMISSION_DOCUMENT_TYPE_VIEW], children_view_regex=[r'^document_type_'])
document_type_document_list = Link(text=_(u'documents of this type'), view='document_type_document_list', args='document_type.id', sprite='page_go', permissions=[PERMISSION_DOCUMENT_TYPE_VIEW])
document_type_edit = Link(text=_(u'edit'), view='document_type_edit', args='document_type.id', sprite='layout_edit', permissions=[PERMISSION_DOCUMENT_TYPE_EDIT])
document_type_delete = Link(text=_(u'delete'), view='document_type_delete', args='document_type.id', sprite='layout_delete', permissions=[PERMISSION_DOCUMENT_TYPE_DELETE])
document_type_create = Link(text=_(u'create document type'), view='document_type_create', sprite='layout_add', permissions=[PERMISSION_DOCUMENT_TYPE_CREATE])

document_type_filename_list = Link(text=_(u'filenames'), view='document_type_filename_list', args='document_type.id', sprite='database', permissions=[PERMISSION_DOCUMENT_TYPE_VIEW])
document_type_filename_create = Link(text=_(u'add filename to document type'), view='document_type_filename_create', args='document_type.id', sprite='database_add', permissions=[PERMISSION_DOCUMENT_TYPE_EDIT])
document_type_filename_edit = Link(text=_(u'edit'), view='document_type_filename_edit', args='filename.id', sprite='database_edit', permissions=[PERMISSION_DOCUMENT_TYPE_EDIT])
document_type_filename_delete = Link(text=_(u'delete'), view='document_type_filename_delete', args='filename.id', sprite='database_delete', permissions=[PERMISSION_DOCUMENT_TYPE_EDIT])

# TODO: remove this
document_type_views = ['setup_document_type_metadata', 'document_type_list', 'document_type_document_list', 'document_type_edit', 'document_type_delete', 'document_type_create', 'document_type_filename_list', 'document_type_filename_create', 'document_type_filename_edit', 'document_type_filename_delete']
