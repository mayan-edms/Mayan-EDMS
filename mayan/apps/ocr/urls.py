from __future__ import unicode_literals

from django.conf.urls import patterns, url

from .api_views import DocumentVersionOCRView

urlpatterns = patterns('ocr.views',
    url(r'^document/(?P<pk>\d+)/submit/$', 'document_submit', (), 'document_submit'),
    url(r'^document/multiple/submit/$', 'document_submit_multiple', (), 'document_submit_multiple'),
    url(r'^document/all/clean_up/$', 'document_all_ocr_cleanup', (), 'document_all_ocr_cleanup'),

    url(r'^all/$', 'entry_list', (), 'entry_list'),
    url(r'^(?P<pk>\d+)/delete/$', 'entry_delete', (), 'entry_delete'),
    url(r'^multiple/delete/$', 'entry_delete_multiple', (), 'entry_delete_multiple'),
    url(r'^(?P<pk>\d+)/re-queue/$', 'entry_re_queue', (), 'entry_re_queue'),
    url(r'^multiple/re-queue/$', 'entry_re_queue_multiple', (), 'entry_re_queue_multiple'),
)

api_urls = patterns('',
    url(r'^submit/$', DocumentVersionOCRView.as_view(), name='document-version-ocr-submit-view'),
)
