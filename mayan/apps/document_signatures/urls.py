from __future__ import unicode_literals

from django.conf.urls import patterns, url

from .views import (
    DocumentVersionSignatureDeleteView, DocumentVersionSignatureDetailView,
    DocumentVersionSignatureListView, DocumentVersionSignatureUploadView
)

urlpatterns = patterns(
    'document_signatures.views',
    url(
        r'^(?P<pk>\d+)/details/$',
        DocumentVersionSignatureDetailView.as_view(),
        name='document_version_signature_details'
    ),
    url(
        r'^signature/(?P<pk>\d+)/download/$',
        'document_signature_download',
        name='document_version_signature_download'
    ),
    url(
        r'^document/version/(?P<pk>\d+)/signatures/list/$',
        DocumentVersionSignatureListView.as_view(),
        name='document_version_signature_list'
    ),
    url(
        r'^documents/version/(?P<pk>\d+)/signature/upload/$',
        DocumentVersionSignatureUploadView.as_view(),
        name='document_version_signature_upload'
    ),
    url(
        r'^signature/(?P<pk>\d+)/delete/$',
        DocumentVersionSignatureDeleteView.as_view(),
        name='document_version_signature_delete'
    ),
)
