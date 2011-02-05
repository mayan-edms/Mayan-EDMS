from django.conf.urls.defaults import *
from django.utils.translation import ugettext_lazy as _
from django.views.generic.create_update import create_object, update_object


urlpatterns = patterns('documents.views',
    url(r'^document/list/$', 'document_list', (), 'document_list'),
    url(r'^document/create/single/$', 'document_create', {'multiple':False}, 'document_create'),
    url(r'^document/create/multiple/$', 'document_create', {'multiple':True}, 'document_create_multiple'),
    url(r'^document/type/(?P<document_type_id>\d+)/upload/single/$', 'upload_document_with_type', {'multiple':False}, 'upload_document_with_type'),
    url(r'^document/type/(?P<document_type_id>\d+)/upload/multiple/$', 'upload_document_with_type', {'multiple':True}, 'upload_multiple_documents_with_type'),
    url(r'^document/(?P<document_id>\d+)/$', 'document_view', (), 'document_view'),
    url(r'^document/(?P<document_id>\d+)/delete/$', 'document_delete', (), 'document_delete'),
)
