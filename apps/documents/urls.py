from django.conf.urls.defaults import *
from django.utils.translation import ugettext_lazy as _
from django.views.generic.create_update import create_object, update_object


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
    url(r'^document/(?P<document_id>\d+)/preview/$', 'document_preview', (), 'document_preview'),
    url(r'^document/(?P<document_id>\d+)/thumbnail/$', 'document_thumbnail', (), 'document_thumbnail'),
    url(r'^document/(?P<document_id>\d+)/download/$', 'document_download', (), 'document_download'),
    url(r'^document/(?P<document_id>\d+)/create/siblings/$', 'document_create_sibling', {'multiple':True}, 'document_create_sibling'),
    
    url(r'^staging_file/(?P<staging_file_id>\w+)/preview/$', 'staging_file_preview', (), 'staging_file_preview'),


)
