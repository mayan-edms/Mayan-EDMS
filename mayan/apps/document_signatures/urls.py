from __future__ import unicode_literals

from django.conf.urls import patterns, url

urlpatterns = patterns(
    'document_signatures.views',
    url(
        r'^verify/(?P<document_pk>\d+)/$', 'document_verify',
        name='document_verify'
    ),
    url(
        r'^upload/signature/(?P<document_pk>\d+)/$',
        'document_signature_upload', name='document_signature_upload'
    ),
    url(
        r'^download/signature/(?P<document_pk>\d+)/$',
        'document_signature_download', name='document_signature_download'
    ),
    url(
        r'^document/(?P<document_pk>\d+)/signature/delete/$',
        'document_signature_delete', name='document_signature_delete'
    ),
)
