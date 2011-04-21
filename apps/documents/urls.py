from django.conf.urls.defaults import patterns, url
from django.utils.translation import ugettext_lazy as _
from django.views.generic.create_update import create_object, update_object

from documents.conf.settings import PREVIEW_SIZE
from documents.conf.settings import THUMBNAIL_SIZE
from documents.conf.settings import DISPLAY_SIZE
from documents.conf.settings import MULTIPAGE_PREVIEW_SIZE
from documents.conf.settings import ENABLE_SINGLE_DOCUMENT_UPLOAD

from converter.api import QUALITY_HIGH


urlpatterns = patterns('documents.views',
    url(r'^document/list/$', 'document_list', (), 'document_list'),
    url(r'^document/list/recent/$', 'document_list_recent', (), 'document_list_recent'),
    url(r'^document/create/from/local/single/$', 'document_create', {'multiple': False}, 'document_create'),
    url(r'^document/create/from/local/multiple/$', 'document_create', {'multiple': True}, 'document_create_multiple'),
    url(r'^document/type/(?P<document_type_id>\d+)/upload/single/$', 'upload_document_with_type', {'multiple': False}, 'upload_document_with_type'),
    url(r'^document/type/(?P<document_type_id>\d+)/upload/multiple/$', 'upload_document_with_type', {'multiple': True}, 'upload_multiple_documents_with_type'),
    url(r'^document/(?P<document_id>\d+)/$', 'document_view', (), 'document_view'),
    url(r'^document/(?P<document_id>\d+)/simple/$', 'document_view_simple', (), 'document_view_simple'),
    url(r'^document/(?P<document_id>\d+)/delete/$', 'document_delete', (), 'document_delete'),
    url(r'^document/multiple/delete/$', 'document_multiple_delete', (), 'document_multiple_delete'),
    url(r'^document/(?P<document_id>\d+)/edit/$', 'document_edit', (), 'document_edit'),
    url(r'^document/(?P<document_id>\d+)/edit/metadata/$', 'document_edit_metadata', (), 'document_edit_metadata'),
    url(r'^document/multiple/edit/metadata/$', 'document_multiple_edit_metadata', (), 'document_multiple_edit_metadata'),

    url(r'^document/(?P<document_id>\d+)/display/preview/$', 'get_document_image', {'size': PREVIEW_SIZE}, 'document_preview'),
    url(r'^document/(?P<document_id>\d+)/display/preview/multipage/$', 'get_document_image', {'size': MULTIPAGE_PREVIEW_SIZE}, 'document_preview_multipage'),
    url(r'^document/(?P<document_id>\d+)/display/thumbnail/$', 'get_document_image', {'size': THUMBNAIL_SIZE}, 'document_thumbnail'),
    url(r'^document/(?P<document_id>\d+)/display/$', 'get_document_image', {'size': DISPLAY_SIZE, 'quality': QUALITY_HIGH}, 'document_display'),

    url(r'^document/(?P<document_id>\d+)/download/$', 'document_download', (), 'document_download'),
    url(r'^document/(?P<document_id>\d+)/create/siblings/$', 'document_create_sibling', {'multiple': True if ENABLE_SINGLE_DOCUMENT_UPLOAD == False else False}, 'document_create_sibling'),
    url(r'^document/(?P<document_id>\d+)/find_duplicates/$', 'document_find_duplicates', (), 'document_find_duplicates'),
    url(r'^document/(?P<document_id>\d+)/clear_transformations/$', 'document_clear_transformations', (), 'document_clear_transformations'),
    url(r'^document/multiple/clear_transformations/$', 'document_multiple_clear_transformations', (), 'document_multiple_clear_transformations'),
    url(r'^duplicates/$', 'document_find_all_duplicates', (), 'document_find_all_duplicates'),

    url(r'^staging_file/(?P<staging_file_id>\w+)/preview/$', 'staging_file_preview', (), 'staging_file_preview'),
    url(r'^staging_file/(?P<staging_file_id>\w+)/delete/$', 'staging_file_delete', (), 'staging_file_delete'),

    url(r'^document/page/(?P<document_page_id>\d+)/$', 'document_page_view', (), 'document_page_view'),
    url(r'^document/page/(?P<document_page_id>\d+)/text/$', 'document_page_text', (), 'document_page_text'),
    url(r'^document/page/(?P<document_page_id>\d+)/edit/$', 'document_page_edit', (), 'document_page_edit'),
    url(r'^document/page/(?P<document_page_id>\d+)/navigation/next/$', 'document_page_navigation_next', (), 'document_page_navigation_next'),
    url(r'^document/page/(?P<document_page_id>\d+)/navigation/previous/$', 'document_page_navigation_previous', (), 'document_page_navigation_previous'),
    url(r'^document/page/(?P<document_page_id>\d+)/navigation/first/$', 'document_page_navigation_first', (), 'document_page_navigation_first'),
    url(r'^document/page/(?P<document_page_id>\d+)/navigation/last/$', 'document_page_navigation_last', (), 'document_page_navigation_last'),
    url(r'^document/page/(?P<document_page_id>\d+)/zoom/in/$', 'document_page_zoom_in', (), 'document_page_zoom_in'),
    url(r'^document/page/(?P<document_page_id>\d+)/zoom/out/$', 'document_page_zoom_out', (), 'document_page_zoom_out'),

    url(r'^document/page/(?P<document_page_id>\d+)/transformation/list/$', 'document_page_transformation_list', (), 'document_page_transformation_list'),
    url(r'^document/page/(?P<document_page_id>\d+)/transformation/create/$', 'document_page_transformation_create', (), 'document_page_transformation_create'),
    
    url(r'^document/page/transformation/(?P<document_page_transformation_id>\d+)/edit/$', 'document_page_transformation_edit', (), 'document_page_transformation_edit'),
    url(r'^document/page/transformation/(?P<document_page_transformation_id>\d+)/delete/$', 'document_page_transformation_delete', (), 'document_page_transformation_delete'),

    url(r'^document/missing/list/$', 'document_missing_list', (), 'document_missing_list'),
)
