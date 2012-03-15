from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('document_signatures.views',
    url(r'^document/(?P<document_pk>\d+)/signature/verify/$', 'document_verify', (), 'document_verify'),
    url(r'^document/(?P<document_pk>\d+)/signature/upload/$', 'document_signature_upload', (), 'document_signature_upload'),
    url(r'^document/(?P<document_pk>\d+)/signature/download/$', 'document_signature_download', (), 'document_signature_download'),
    url(r'^document/(?P<document_pk>\d+)/signature/delete/$', 'document_signature_delete', (), 'document_signature_delete'),
)
