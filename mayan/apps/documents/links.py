from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from events.permissions import PERMISSION_EVENTS_VIEW
from navigation import Link

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


# Facet
link_document_preview = Link(permissions=[PERMISSION_DOCUMENT_VIEW], text=_('Preview'), view='documents:document_preview', args='object.id')
link_document_content = Link(permissions=[PERMISSION_DOCUMENT_VIEW], text=_('Content'), view='documents:document_content', args='object.id')
link_document_properties = Link(permissions=[PERMISSION_DOCUMENT_VIEW], text=_('Properties'), view='documents:document_properties', args='object.id')
link_document_events_view = Link(permissions=[PERMISSION_EVENTS_VIEW], text=_('Events'), view='events:events_for_object', args=['"documents"', '"document"', 'object.id'])
link_document_version_list = Link(permissions=[PERMISSION_DOCUMENT_VIEW], text=_('Versions'), view='documents:document_version_list', args='object.pk')

# Actions
link_document_clear_transformations = Link(permissions=[PERMISSION_DOCUMENT_TRANSFORM], text=_('Clear transformations'), view='documents:document_clear_transformations', args='object.id')
link_document_delete = Link(permissions=[PERMISSION_DOCUMENT_DELETE], text=_('Delete'), view='documents:document_delete', args='object.id')
link_document_edit = Link(permissions=[PERMISSION_DOCUMENT_PROPERTIES_EDIT], text=_('Edit properties'), view='documents:document_edit', args='object.id')
link_document_document_type_edit = Link(permissions=[PERMISSION_DOCUMENT_PROPERTIES_EDIT], text=_('Change type'), view='documents:document_document_type_edit', args='object.id')
link_document_download = Link(permissions=[PERMISSION_DOCUMENT_DOWNLOAD], text=_('Download'), view='documents:document_download', args='object.id')
link_document_print = Link(permissions=[PERMISSION_DOCUMENT_VIEW], text=_('Print'), view='documents:document_print', args='object.id')
link_document_update_page_count = Link(permissions=[PERMISSION_DOCUMENT_TOOLS], text=_('Reset page count'), view='documents:document_update_page_count', args='object.pk')

# Views
link_document_list = Link(icon='fa fa-file', text=_('All documents'), view='documents:document_list')
link_document_list_recent = Link(icon='fa fa-clock-o', text=_('Recent documents'), view='documents:document_list_recent')
link_document_multiple_delete = Link(permissions=[PERMISSION_DOCUMENT_DELETE], text=_('Delete'), view='documents:document_multiple_delete')
link_document_multiple_document_type_edit = Link(permissions=[PERMISSION_DOCUMENT_PROPERTIES_EDIT], text=_('Change type'), view='documents:document_multiple_document_type_edit')
link_document_multiple_download = Link(permissions=[PERMISSION_DOCUMENT_DOWNLOAD], text=_('Download'), view='documents:document_multiple_download')
link_document_version_download = Link(args='object.pk', permissions=[PERMISSION_DOCUMENT_DOWNLOAD], text=_('Download'), view='documents:document_version_download')
link_document_multiple_update_page_count = Link(permissions=[PERMISSION_DOCUMENT_TOOLS], text=_('Reset page count'), view= 'documents:document_multiple_update_page_count')
link_document_multiple_clear_transformations = Link(permissions=[PERMISSION_DOCUMENT_TRANSFORM], text=_('Clear transformations'), view='documents:document_multiple_clear_transformations')

# Tools
link_clear_image_cache = Link(
    description=_('Clear the graphics representations used to speed up the documents\' display and interactive transformations results.'),
    permissions=[PERMISSION_DOCUMENT_TOOLS], text=_('Clear the document image cache'),
    view='documents:document_clear_image_cache'
)

# Document pages
link_document_page_transformation_list = Link(args='page.pk', class='no-parent-history', permissions=[PERMISSION_DOCUMENT_TRANSFORM], text=_('Page transformations'), view='documents:document_page_transformation_list')
link_document_page_transformation_create = Link(args='page.pk', class='no-parent-history', permissions=[PERMISSION_DOCUMENT_TRANSFORM], text= _('Create new transformation'), view='documents:document_page_transformation_create')
link_document_page_transformation_edit = Link(args='transformation.pk', class='no-parent-history', permissions=[PERMISSION_DOCUMENT_TRANSFORM], text=_('Edit'), view='documents:document_page_transformation_edit')
link_document_page_transformation_delete = Link(args='transformation.pk', class='no-parent-history', permissions=[PERMISSION_DOCUMENT_TRANSFORM], text=_('Delete'), view='documents:document_page_transformation_delete')
link_document_page_view = Link(args='page.pk', class='no-parent-history', permissions=[PERMISSION_DOCUMENT_VIEW], text=_('Page image'), view='documents:document_page_view')
link_document_page_text = Link(args='page.pk', class='no-parent-history', permissions=[PERMISSION_DOCUMENT_VIEW], text=_('Page text'), view='documents:document_page_text')
link_document_page_edit = Link(class='no-parent-history', permissions=[PERMISSION_DOCUMENT_EDIT], text=_('Edit page text'), view='documents:document_page_edit', args='page.pk')
link_document_page_navigation_next = Link(text=_('Next page'), 'class': 'no-parent-history', 'view': 'documents:document_page_navigation_next', 'args': 'page.pk', 'famfam': 'resultset_next', 'permissions': [PERMISSION_DOCUMENT_VIEW], 'conditional_disable': is_last_page, 'keep_query': True}
link_document_page_navigation_previous = Link(text=_('Previous page'), 'class': 'no-parent-history', 'view': 'documents:document_page_navigation_previous', 'args': 'page.pk', 'famfam': 'resultset_previous', 'permissions': [PERMISSION_DOCUMENT_VIEW], 'conditional_disable': is_first_page, 'keep_query': True}
link_document_page_navigation_first = Link(text=_('First page'), 'class': 'no-parent-history', 'view': 'documents:document_page_navigation_first', 'args': 'page.pk', 'famfam': 'resultset_first', 'permissions': [PERMISSION_DOCUMENT_VIEW], 'conditional_disable': is_first_page, 'keep_query': True}
link_document_page_navigation_last = Link(text=_('Last page'), 'class': 'no-parent-history', 'view': 'documents:document_page_navigation_last', 'args': 'page.pk', 'famfam': 'resultset_last', 'permissions': [PERMISSION_DOCUMENT_VIEW], 'conditional_disable': is_last_page, 'keep_query': True}
link_document_page_zoom_in = Link(text=_('Zoom in'), 'class': 'no-parent-history', 'view': 'documents:document_page_zoom_in', 'args': 'page.pk', 'famfam': 'zoom_in', 'permissions': [PERMISSION_DOCUMENT_VIEW], 'conditional_disable': is_max_zoom}
link_document_page_zoom_out = Link(text=_('Zoom out'), 'class': 'no-parent-history', 'view': 'documents:document_page_zoom_out', 'args': 'page.pk', 'famfam': 'zoom_out', 'permissions': [PERMISSION_DOCUMENT_VIEW], 'conditional_disable': is_min_zoom}
link_document_page_rotate_right = Link(text=_('Rotate right'), 'class': 'no-parent-history', 'view': 'documents:document_page_rotate_right', 'args': 'page.pk', 'famfam': 'arrow_turn_right', 'permissions': [PERMISSION_DOCUMENT_VIEW]}
link_document_page_rotate_left = Link(text=_('Rotate left'), 'class': 'no-parent-history', 'view': 'documents:document_page_rotate_left', 'args': 'page.pk', 'famfam': 'arrow_turn_left', 'permissions': [PERMISSION_DOCUMENT_VIEW]}
link_document_page_view_reset = Link(text=_('Reset view'), 'class': 'no-parent-history', 'view': 'documents:document_page_view_reset', 'args': 'page.pk', 'famfam': 'page_white', 'permissions': [PERMISSION_DOCUMENT_VIEW]}

# Document versions
document_version_revert = {'text': _('Revert'), 'view': 'documents:document_version_revert', 'args': 'object.pk', 'famfam': 'page_refresh', 'permissions': [PERMISSION_DOCUMENT_VERSION_REVERT], 'conditional_disable': is_current_version}

# Document type related links
document_type_list = {'text': _('Document types'), 'view': 'documents:document_type_list', 'famfam': 'layout', 'permissions': [PERMISSION_DOCUMENT_TYPE_VIEW]}
link_document_type_setup = Link(icon='fa fa-file', permissions=[PERMISSION_DOCUMENT_TYPE_VIEW], text=_('Document types'), view='documents:document_type_list')
document_type_edit = {'text': _('Edit'), 'view': 'documents:document_type_edit', 'args': 'document_type.id', 'famfam': 'layout_edit', 'permissions': [PERMISSION_DOCUMENT_TYPE_EDIT]}
document_type_delete = {'text': _('Delete'), 'view': 'documents:document_type_delete', 'args': 'document_type.id', 'famfam': 'layout_delete', 'permissions': [PERMISSION_DOCUMENT_TYPE_DELETE]}
document_type_create = {'text': _('Create document type'), 'view': 'documents:document_type_create', 'famfam': 'layout_add', 'permissions': [PERMISSION_DOCUMENT_TYPE_CREATE]}

document_type_filename_list = {'text': _('Filenames'), 'view': 'documents:document_type_filename_list', 'args': 'document_type.id', 'famfam': 'database', 'permissions': [PERMISSION_DOCUMENT_TYPE_VIEW]}
document_type_filename_create = {'text': _('Add filename to document type'), 'view': 'documents:document_type_filename_create', 'args': 'document_type.id', 'famfam': 'database_add', 'permissions': [PERMISSION_DOCUMENT_TYPE_EDIT]}
document_type_filename_edit = {'text': _('Edit'), 'view': 'documents:document_type_filename_edit', 'args': 'filename.id', 'famfam': 'database_edit', 'permissions': [PERMISSION_DOCUMENT_TYPE_EDIT]}
document_type_filename_delete = {'text': _('Delete'), 'view': 'documents:document_type_filename_delete', 'args': 'filename.id', 'famfam': 'database_delete', 'permissions': [PERMISSION_DOCUMENT_TYPE_EDIT]}
