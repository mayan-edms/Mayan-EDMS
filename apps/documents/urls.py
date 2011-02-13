from django.conf.urls.defaults import *
from django.utils.translation import ugettext_lazy as _
from django.views.generic.create_update import create_object, update_object

from documents.conf.settings import PREVIEW_SIZE
from documents.conf.settings import THUMBNAIL_SIZE
from documents.conf.settings import DISPLAY_SIZE

from converter.api import QUALITY_HIGH


urlpatterns = patterns('documents.views',
    url(r'^document/list/$', 'document_list', (), 'document_list'),
    url(r'^document/create/from/local/single/$', 'document_create', {'multiple':False}, 'document_create'),
    url(r'^document/create/from/local/multiple/$', 'document_create', {'multiple':True}, 'document_create_multiple'),
    url(r'^document/type/(?P<document_type_id>\d+)/upload/single/$', 'upload_document_with_type', {'multiple':False}, 'upload_document_with_type'),
    url(r'^document/type/(?P<document_type_id>\d+)/upload/multiple/$', 'upload_document_with_type', {'multiple':True}, 'upload_multiple_documents_with_type'),
    url(r'^document/(?P<document_id>\d+)/$', 'document_view', (), 'document_view'),
    url(r'^document/(?P<document_id>\d+)/delete/$', 'document_delete', (), 'document_delete'),
    url(r'^document/(?P<document_id>\d+)/edit/$', 'document_edit', (), 'document_edit'),
    url(r'^document/(?P<document_id>\d+)/edit/metadata/$', 'document_edit_metadata', (), 'document_edit_metadata'),
    url(r'^document/(?P<document_id>\d+)/preview/$', 'get_document_image', {'size':PREVIEW_SIZE}, 'document_preview'),
    url(r'^document/(?P<document_id>\d+)/thumbnail/$', 'get_document_image', {'size':THUMBNAIL_SIZE}, 'document_thumbnail'),
    url(r'^document/(?P<document_id>\d+)/display/$', 'get_document_image', {'size':DISPLAY_SIZE,'quality':QUALITY_HIGH}, 'document_display'),
    url(r'^document/(?P<document_id>\d+)/download/$', 'document_download', (), 'document_download'),
    url(r'^document/(?P<document_id>\d+)/create/siblings/$', 'document_create_sibling', {'multiple':False}, 'document_create_sibling'),

    url(r'^document/(?P<document_id>\d+)/tranformation/list/$', 'document_transformation_list', (), 'document_transformation_list'),
    url(r'^document/tranformation/(?P<document_transformation_id>\d+)/delete/$', 'document_transformation_delete', (), 'document_transformation_delete'),

    
    url(r'^staging_file/(?P<staging_file_id>\w+)/preview/$', 'staging_file_preview', (), 'staging_file_preview'),
    url(r'^staging_file/(?P<staging_file_id>\w+)/delete/$', 'staging_file_delete', (), 'staging_file_delete'),
)
