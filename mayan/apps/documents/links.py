from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from acls.permissions import ACLS_VIEW_ACL
from events.permissions import PERMISSION_EVENTS_VIEW
from navigation import Link

from .permissions import (
    PERMISSION_DOCUMENT_DELETE, PERMISSION_DOCUMENT_DOWNLOAD,
    PERMISSION_DOCUMENT_EDIT, PERMISSION_DOCUMENT_PROPERTIES_EDIT,
    PERMISSION_DOCUMENT_PRINT, PERMISSION_DOCUMENT_TRANSFORM,
    PERMISSION_DOCUMENT_TOOLS, PERMISSION_DOCUMENT_VERSION_REVERT,
    PERMISSION_DOCUMENT_VIEW, PERMISSION_DOCUMENT_TYPE_CREATE,
    PERMISSION_DOCUMENT_TYPE_DELETE, PERMISSION_DOCUMENT_TYPE_EDIT,
    PERMISSION_DOCUMENT_TYPE_VIEW
)
from .settings import ZOOM_MAX_LEVEL, ZOOM_MIN_LEVEL


def is_not_current_version(context):
    return context['object'].document.latest_version.timestamp != context['object'].timestamp


def is_first_page(context):
    return context['page'].page_number <= 1


def is_last_page(context):
    return context['page'].page_number >= context['page'].document_version.pages.count()


def is_max_zoom(context):
    return context['zoom'] >= ZOOM_MAX_LEVEL


def is_min_zoom(context):
    return context['zoom'] <= ZOOM_MIN_LEVEL


# Facet
link_document_acl_list = Link(permissions=[ACLS_VIEW_ACL], text=_('ACLs'), view='documents:document_acl_list', args='object.pk')
link_document_content = Link(permissions=[PERMISSION_DOCUMENT_VIEW], text=_('Content'), view='documents:document_content', args='object.id')
link_document_events_view = Link(permissions=[PERMISSION_EVENTS_VIEW], text=_('Events'), view='events:events_for_object', args=['"documents"', '"document"', 'object.id'])
link_document_preview = Link(permissions=[PERMISSION_DOCUMENT_VIEW], text=_('Preview'), view='documents:document_preview', args='object.id')
link_document_properties = Link(permissions=[PERMISSION_DOCUMENT_VIEW], text=_('Properties'), view='documents:document_properties', args='object.id')
link_document_version_list = Link(permissions=[PERMISSION_DOCUMENT_VIEW], text=_('Versions'), view='documents:document_version_list', args='object.pk')

# Actions
link_document_clear_transformations = Link(permissions=[PERMISSION_DOCUMENT_TRANSFORM], text=_('Clear transformations'), view='documents:document_clear_transformations', args='object.id')
link_document_delete = Link(permissions=[PERMISSION_DOCUMENT_DELETE], tags='dangerous', text=_('Delete'), view='documents:document_delete', args='object.id')
link_document_edit = Link(permissions=[PERMISSION_DOCUMENT_PROPERTIES_EDIT], text=_('Edit properties'), view='documents:document_edit', args='object.id')
link_document_document_type_edit = Link(permissions=[PERMISSION_DOCUMENT_PROPERTIES_EDIT], text=_('Change type'), view='documents:document_document_type_edit', args='object.id')
link_document_download = Link(permissions=[PERMISSION_DOCUMENT_DOWNLOAD], text=_('Download'), view='documents:document_download', args='object.id')
link_document_print = Link(permissions=[PERMISSION_DOCUMENT_PRINT], text=_('Print'), view='documents:document_print', args='object.id')
link_document_update_page_count = Link(permissions=[PERMISSION_DOCUMENT_TOOLS], text=_('Reset page count'), view='documents:document_update_page_count', args='object.pk')

# Views
link_document_list = Link(icon='fa fa-file', text=_('All documents'), view='documents:document_list')
link_document_list_recent = Link(icon='fa fa-clock-o', text=_('Recent documents'), view='documents:document_list_recent')
link_document_multiple_clear_transformations = Link(permissions=[PERMISSION_DOCUMENT_TRANSFORM], text=_('Clear transformations'), view='documents:document_multiple_clear_transformations')
link_document_multiple_delete = Link(permissions=[PERMISSION_DOCUMENT_DELETE], tags='dangerous', text=_('Delete'), view='documents:document_multiple_delete')
link_document_multiple_document_type_edit = Link(permissions=[PERMISSION_DOCUMENT_PROPERTIES_EDIT], text=_('Change type'), view='documents:document_multiple_document_type_edit')
link_document_multiple_download = Link(permissions=[PERMISSION_DOCUMENT_DOWNLOAD], text=_('Download'), view='documents:document_multiple_download')
link_document_multiple_update_page_count = Link(permissions=[PERMISSION_DOCUMENT_TOOLS], text=_('Reset page count'), view= 'documents:document_multiple_update_page_count')
link_document_version_download = Link(args='object.pk', permissions=[PERMISSION_DOCUMENT_DOWNLOAD], text=_('Download'), view='documents:document_version_download')

# Tools
link_clear_image_cache = Link(
    description=_('Clear the graphics representations used to speed up the documents\' display and interactive transformations results.'),
    permissions=[PERMISSION_DOCUMENT_TOOLS], text=_('Clear the document image cache'),
    view='documents:document_clear_image_cache'
)

# Document pages
link_document_page_transformation_create = Link(args='page.pk', permissions=[PERMISSION_DOCUMENT_TRANSFORM], text= _('Create new transformation'), view='documents:document_page_transformation_create')
link_document_page_transformation_delete = Link(args='transformation.pk', permissions=[PERMISSION_DOCUMENT_TRANSFORM], tags='dangerous', text=_('Delete'), view='documents:document_page_transformation_delete')
link_document_page_transformation_edit = Link(args='transformation.pk', permissions=[PERMISSION_DOCUMENT_TRANSFORM], text=_('Edit'), view='documents:document_page_transformation_edit')
link_document_page_transformation_list = Link(args='page.pk', permissions=[PERMISSION_DOCUMENT_TRANSFORM], text=_('Transformations'), view='documents:document_page_transformation_list')
link_document_page_navigation_first = Link(conditional_disable=is_first_page, icon='fa fa-step-backward', keep_query=True, permissions=[PERMISSION_DOCUMENT_VIEW], text=_('First page'), view='documents:document_page_navigation_first', args='page.pk')
link_document_page_navigation_last = Link(conditional_disable=is_last_page, icon='fa fa-step-forward', keep_query=True, text=_('Last page'), permissions=[PERMISSION_DOCUMENT_VIEW], view='documents:document_page_navigation_last', args='page.pk')
link_document_page_navigation_previous = Link(conditional_disable=is_first_page, icon='fa fa-arrow-left', keep_query=True, permissions=[PERMISSION_DOCUMENT_VIEW], text=_('Previous page'), view='documents:document_page_navigation_previous', args='page.pk')
link_document_page_navigation_next = Link(conditional_disable=is_last_page, icon='fa fa-arrow-right', keep_query=True, text=_('Next page'), permissions=[PERMISSION_DOCUMENT_VIEW], view='documents:document_page_navigation_next', args='page.pk')
link_document_page_return = Link(icon='fa fa-file', permissions=[PERMISSION_DOCUMENT_VIEW], text=_('Document'), view='documents:document_preview', args='page.document.pk')
link_document_page_rotate_left = Link(icon='fa fa-rotate-left', permissions=[PERMISSION_DOCUMENT_VIEW], text=_('Rotate left'), view='documents:document_page_rotate_left', args='page.pk')
link_document_page_rotate_right = Link(icon='fa fa-rotate-right', permissions=[PERMISSION_DOCUMENT_VIEW], text=_('Rotate right'), view='documents:document_page_rotate_right', args='page.pk')
link_document_page_view = Link(args='page.pk', permissions=[PERMISSION_DOCUMENT_VIEW], text=_('Page image'), view='documents:document_page_view')
link_document_page_view_reset = Link(permissions=[PERMISSION_DOCUMENT_VIEW], text=_('Reset view'), view='documents:document_page_view_reset', args='page.pk')
link_document_page_zoom_in = Link(conditional_disable=is_max_zoom, icon='fa fa-search-plus', permissions=[PERMISSION_DOCUMENT_VIEW], text=_('Zoom in'), view='documents:document_page_zoom_in', args='page.pk')
link_document_page_zoom_out = Link(conditional_disable=is_min_zoom, icon='fa fa-search-minus', permissions=[PERMISSION_DOCUMENT_VIEW], text=_('Zoom out'), view='documents:document_page_zoom_out', args='page.pk')

# Document versions
link_document_version_revert = Link(condition=is_not_current_version, permissions=[PERMISSION_DOCUMENT_VERSION_REVERT], tags='dangerous', text=_('Revert'), view='documents:document_version_revert', args='object.pk')

# Document type related links
link_document_type_create = Link(permissions=[PERMISSION_DOCUMENT_TYPE_CREATE], text=_('Create document type'), view='documents:document_type_create')
link_document_type_delete = Link(permissions=[PERMISSION_DOCUMENT_TYPE_DELETE], tags='dangerous', text=_('Delete'), view='documents:document_type_delete', args='resolved_object.id')
link_document_type_edit = Link(permissions=[PERMISSION_DOCUMENT_TYPE_EDIT], text=_('Edit'), view='documents:document_type_edit', args='resolved_object.id')
link_document_type_filename_create = Link(permissions=[PERMISSION_DOCUMENT_TYPE_EDIT], text=_('Add filename to document type'), view='documents:document_type_filename_create', args='document_type.id')
link_document_type_filename_delete = Link(permissions=[PERMISSION_DOCUMENT_TYPE_EDIT], tags='dangerous', text=_('Delete'), view='documents:document_type_filename_delete', args='resolved_object.id')
link_document_type_filename_edit = Link(permissions=[PERMISSION_DOCUMENT_TYPE_EDIT], text=_('Edit'), view='documents:document_type_filename_edit', args='resolved_object.id')
link_document_type_filename_list = Link(permissions=[PERMISSION_DOCUMENT_TYPE_VIEW], text=_('Filenames'), view='documents:document_type_filename_list', args='resolved_object.id')
link_document_type_list = Link(permissions=[PERMISSION_DOCUMENT_TYPE_VIEW], text=_('Document types'), view='documents:document_type_list')
link_document_type_setup = Link(icon='fa fa-file', permissions=[PERMISSION_DOCUMENT_TYPE_VIEW], text=_('Document types'), view='documents:document_type_list')
