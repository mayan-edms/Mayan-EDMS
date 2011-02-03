from django.conf.urls.defaults import *
from django.utils.translation import ugettext_lazy as _
from django.views.generic.create_update import create_object, update_object


urlpatterns = patterns('documents.views',
    url(r'^document/list/$', 'document_list', (), 'document_list'),
    url(r'^document/create/$', 'document_create', (), 'document_create'),
    #url(r'^document/upload/$', 'upload_document', (), 'upload_document'),
    url(r'^document/type/(?P<document_type_id>\d+)/upload/$', 'upload_document_with_type', (), 'upload_document_with_type'),
)
