from django.conf.urls.defaults import *
from django.utils.translation import ugettext_lazy as _

urlpatterns = patterns('ocr.views',
    url(r'^(?P<document_id>\d+)/submit/$', 'submit_document', (), 'submit_document'),
    url(r'^ocr/queue/document/list/$', 'queue_document_list', (), 'queue_document_list'),
    url(r'^ocr/queue/document/(?P<queue_document_id>\d+)/delete/$', 'queue_document_delete', (), 'queue_document_delete'),
)
