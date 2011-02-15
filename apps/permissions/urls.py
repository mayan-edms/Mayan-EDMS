from django.conf.urls.defaults import *
#from django.utils.translation import ugettext_lazy as _
#from django.views.generic.create_update import create_object, update_object

urlpatterns = patterns('permissions.views',
    url(r'^role/list/$', 'role_list', (), 'role_list'),
    url(r'^role/(?P<role_id>\d+)/$', 'role_view', (), 'role_view'),
    url(r'^role/create/$', 'role_create', (), 'role_create'),
    url(r'^role/(?P<role_id>\d+)/delete/$', 'role_delete', (), 'role_delete'),

#    url(r'^document/create/from/local/single/$', 'document_create', {'multiple':False}, 'document_create'),
#    url(r'^document/create/from/local/multiple/$', 'document_create', {'multiple':True}, 'document_create_multiple'),
#    url(r'^document/type/(?P<document_type_id>\d+)/upload/single/$', 'upload_document_with_type', {'multiple':False}, 'upload_document_with_type'),
#    url(r'^document/type/(?P<document_type_id>\d+)/upload/multiple/$', 'upload_document_with_type', {'multiple':True}, 'upload_multiple_documents_with_type'),
#    url(r'^document/(?P<document_id>\d+)/edit/$', 'document_edit', (), 'document_edit'),
#    url(r'^document/(?P<document_id>\d+)/edit/metadata/$', 'document_edit_metadata', (), 'document_edit_metadata'),
#    url(r'^document/(?P<document_id>\d+)/display/preview/$', 'get_document_image', {'size':PREVIEW_SIZE}, 'document_preview'),
#    url(r'^document/(?P<document_id>\d+)/display/preview/multipage/$', 'get_document_image', {'size':MULTIPAGE_PREVIEW_SIZE}, 'document_preview_multipage'),
#    url(r'^document/(?P<document_id>\d+)/display/thumbnail/$', 'get_document_image', {'size':THUMBNAIL_SIZE}, 'document_thumbnail'),
#    url(r'^document/(?P<document_id>\d+)/display/$', 'get_document_image', {'size':DISPLAY_SIZE,'quality':QUALITY_HIGH}, 'document_display'),
#    url(r'^document/(?P<document_id>\d+)/download/$', 'document_download', (), 'document_download'),
#    url(r'^document/(?P<document_id>\d+)/create/siblings/$', 'document_create_sibling', {'multiple':False}, 'document_create_sibling'),
)
