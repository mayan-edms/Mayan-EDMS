from __future__ import absolute_import

from django.conf.urls.defaults import patterns, url

from .settings import (PREVIEW_SIZE, PRINT_SIZE, THUMBNAIL_SIZE,
    DISPLAY_SIZE, MULTIPAGE_PREVIEW_SIZE)


urlpatterns = patterns('documents.views',
    url(r'^list/$', 'document_list', (), 'document_list'),
    url(r'^list/recent/$', 'document_list_recent', (), 'document_list_recent'),

    url(r'^(?P<document_id>\d+)/view/$', 'document_view', (), 'document_view_simple'),
    url(r'^(?P<document_id>\d+)/view/advanced/$', 'document_view', {'advanced': True}, 'document_view_advanced'),
    url(r'^(?P<document_id>\d+)/delete/$', 'document_delete', (), 'document_delete'),
    url(r'^multiple/delete/$', 'document_multiple_delete', (), 'document_multiple_delete'),
    url(r'^(?P<document_id>\d+)/edit/$', 'document_edit', (), 'document_edit'),
    url(r'^(?P<document_id>\d+)/print/$', 'document_print', (), 'document_print'),
    url(r'^(?P<document_id>\d+)/hard_copy/$', 'document_hard_copy', (), 'document_hard_copy'),

    url(r'^(?P<document_id>\d+)/display/preview/$', 'get_document_image', {'size': PREVIEW_SIZE}, 'document_preview'),
    url(r'^(?P<document_id>\d+)/display/preview/multipage/$', 'get_document_image', {'size': MULTIPAGE_PREVIEW_SIZE}, 'document_preview_multipage'),
    url(r'^(?P<document_id>\d+)/display/thumbnail/$', 'get_document_image', {'size': THUMBNAIL_SIZE}, 'document_thumbnail'),
    url(r'^(?P<document_id>\d+)/display/$', 'get_document_image', {'size': DISPLAY_SIZE}, 'document_display'),
    url(r'^(?P<document_id>\d+)/display/print/$', 'get_document_image', {'size': PRINT_SIZE}, 'document_display_print'),

    url(r'^(?P<document_id>\d+)/display/preview/base64/$', 'get_document_image', {'size': PREVIEW_SIZE, 'base64_version': True}, 'document_preview_base64'),
    url(r'^(?P<document_id>\d+)/display/preview/multipage/base64/$', 'get_document_image', {'size': MULTIPAGE_PREVIEW_SIZE, 'base64_version': True}, 'document_preview_multipage_base64'),
    url(r'^(?P<document_id>\d+)/display/thumbnail/base64/$', 'get_document_image', {'size': THUMBNAIL_SIZE, 'base64_version': True}, 'document_thumbnail_base64'),

    url(r'^(?P<document_id>\d+)/download/$', 'document_download', (), 'document_download'),
    url(r'^multiple/download/$', 'document_multiple_download', (), 'document_multiple_download'),
    url(r'^(?P<document_id>\d+)/create/siblings/$', 'document_create_siblings', (), 'document_create_siblings'),
    url(r'^(?P<document_id>\d+)/find_duplicates/$', 'document_find_duplicates', (), 'document_find_duplicates'),
    url(r'^(?P<document_id>\d+)/clear_transformations/$', 'document_clear_transformations', (), 'document_clear_transformations'),

    url(r'^(?P<document_pk>\d+)/version/all/$', 'document_version_list', (), 'document_version_list'),
    url(r'^document/version/(?P<document_version_pk>\d+)/download/$', 'document_download', (), 'document_version_download'),
    url(r'^document/version/(?P<document_version_pk>\d+)/revert/$', 'document_version_revert', (), 'document_version_revert'),
    url(r'^document/(?P<document_pk>\d+)/version_compare/text/$', 'document_version_text_compare', (), 'document_version_text_compare'),
    url(r'^document/version/show/text/diff/(?P<left_document_version_pk>\d+)/vs/(?P<right_document_version_pk>\d+)/$', 'document_version_show_diff_text', (), 'document_version_show_diff_text'),

    url(r'^multiple/clear_transformations/$', 'document_multiple_clear_transformations', (), 'document_multiple_clear_transformations'),
    url(r'^duplicates/list/$', 'document_find_all_duplicates', (), 'document_find_all_duplicates'),
    url(r'^maintenance/update_page_count/$', 'document_update_page_count', (), 'document_update_page_count'),
    url(r'^maintenance/clear_image_cache/$', 'document_clear_image_cache', (), 'document_clear_image_cache'),

    url(r'^page/(?P<document_page_id>\d+)/$', 'document_page_view', (), 'document_page_view'),
    url(r'^page/(?P<document_page_id>\d+)/text/$', 'document_page_text', (), 'document_page_text'),
    url(r'^page/(?P<document_page_id>\d+)/edit/$', 'document_page_edit', (), 'document_page_edit'),
    url(r'^page/(?P<document_page_id>\d+)/navigation/next/$', 'document_page_navigation_next', (), 'document_page_navigation_next'),
    url(r'^page/(?P<document_page_id>\d+)/navigation/previous/$', 'document_page_navigation_previous', (), 'document_page_navigation_previous'),
    url(r'^page/(?P<document_page_id>\d+)/navigation/first/$', 'document_page_navigation_first', (), 'document_page_navigation_first'),
    url(r'^page/(?P<document_page_id>\d+)/navigation/last/$', 'document_page_navigation_last', (), 'document_page_navigation_last'),
    url(r'^page/(?P<document_page_id>\d+)/zoom/in/$', 'document_page_zoom_in', (), 'document_page_zoom_in'),
    url(r'^page/(?P<document_page_id>\d+)/zoom/out/$', 'document_page_zoom_out', (), 'document_page_zoom_out'),
    url(r'^page/(?P<document_page_id>\d+)/rotate/right/$', 'document_page_rotate_right', (), 'document_page_rotate_right'),
    url(r'^page/(?P<document_page_id>\d+)/rotate/left/$', 'document_page_rotate_left', (), 'document_page_rotate_left'),
    url(r'^page/(?P<document_page_id>\d+)/reset/$', 'document_page_view_reset', (), 'document_page_view_reset'),

    url(r'^page/(?P<document_page_id>\d+)/transformation/list/$', 'document_page_transformation_list', (), 'document_page_transformation_list'),
    url(r'^page/(?P<document_page_id>\d+)/transformation/create/$', 'document_page_transformation_create', (), 'document_page_transformation_create'),

    url(r'^page/transformation/(?P<document_page_transformation_id>\d+)/edit/$', 'document_page_transformation_edit', (), 'document_page_transformation_edit'),
    url(r'^page/transformation/(?P<document_page_transformation_id>\d+)/delete/$', 'document_page_transformation_delete', (), 'document_page_transformation_delete'),

    url(r'^missing/list/$', 'document_missing_list', (), 'document_missing_list'),

    # Admin views
    url(r'^type/list/$', 'document_type_list', (), 'document_type_list'),
    url(r'^type/create/$', 'document_type_create', (), 'document_type_create'),
    url(r'^type/(?P<document_type_id>\d+)/list/documents/$', 'document_type_document_list', (), 'document_type_document_list'),
    url(r'^type/(?P<document_type_id>\d+)/edit/$', 'document_type_edit', (), 'document_type_edit'),
    url(r'^type/(?P<document_type_id>\d+)/delete/$', 'document_type_delete', (), 'document_type_delete'),

    url(r'^type/(?P<document_type_id>\d+)/filename/list/$', 'document_type_filename_list', (), 'document_type_filename_list'),
    url(r'^type/filename/(?P<document_type_filename_id>\d+)/edit/$', 'document_type_filename_edit', (), 'document_type_filename_edit'),
    url(r'^type/filename/(?P<document_type_filename_id>\d+)/delete/$', 'document_type_filename_delete', (), 'document_type_filename_delete'),
    url(r'^type/(?P<document_type_id>\d+)/filename/create/$', 'document_type_filename_create', (), 'document_type_filename_create'),

)
