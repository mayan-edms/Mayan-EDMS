from __future__ import absolute_import

from django.conf.urls import url

from .cleanup import cleanup
from .api import APIDocumentView, APIDocumentVersionView, APIDocumentImageView, APIDocumentPageView

bootstrap_models = [
    {
        'name': 'documenttype',
    },
    {
        'name': 'documenttypefilename',
        'dependencies': ['documents.documenttype']
    }
]
cleanup_functions = [cleanup]

version_0_api_services = [
    {'urlpattern': url(r'^document/(?P<pk>[0-9]+)/$', APIDocumentView.as_view(), name='document-detail'), 'description': 'Show document data', 'url': 'document/<document ID>'},
    {'urlpattern': url(r'^document_version/(?P<pk>[0-9]+)/$', APIDocumentVersionView.as_view(), name='documentversion-detail'), 'description': '', 'url': 'document_version/<document_version ID>'},
    {'urlpattern': url(r'^document_page/(?P<pk>[0-9]+)/$', APIDocumentPageView.as_view(), name='documentpage-detail'), 'description': '', 'url': 'document_page/<document page_ID>'},
    {'urlpattern': url(r'^document/(?P<pk>[0-9]+)/image/$', APIDocumentImageView.as_view(), name='document-image'), 'description': 'Return a base64 image of the document', 'url': 'document/<document_id>/image/?page=<page number>&zoom=<zoom percent>&rotate=<rotation degrees>'},
]
