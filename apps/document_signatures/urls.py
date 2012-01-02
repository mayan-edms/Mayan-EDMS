from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('document_signatures.views',
    url(r'^verify/(?P<document_pk>\d+)/$', 'document_verify', (), 'document_verify'),
    url(r'^upload/signature/(?P<document_pk>\d+)/$', 'document_signature_upload', (), 'document_signature_upload'),
    url(r'^download/signature/(?P<document_pk>\d+)/$', 'document_signature_download', (), 'document_signature_download'),
)
