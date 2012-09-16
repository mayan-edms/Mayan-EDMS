from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('ocr.views',
    url(r'^document/(?P<document_id>\d+)/submit/$', 'submit_document', (), 'submit_document'),
    url(r'^document/multiple/submit/$', 'submit_document_multiple', (), 'submit_document_multiple'),

    url(r'^document/all/clean_up/$', 'all_document_ocr_cleanup', (), 'all_document_ocr_cleanup'),
)
