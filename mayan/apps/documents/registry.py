from __future__ import absolute_import

from django.conf.urls import url

from .cleanup import cleanup
from .api import APIReadOnlyInstanceModelView, APIDocumentImageView

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
    {'urlpattern': url(r'^document/(?P<pk>[0-9]+)/$', APIReadOnlyInstanceModelView.as_view(), name='document-detail'), 'description': 'Show document data', 'url': 'document/<document_id>'},
    {'urlpattern': url(r'^document/(?P<pk>[0-9]+)/image/$', APIDocumentImageView.as_view(), name='document-image'), 'description': 'Return a base64 image of the document', 'url': 'document/<document_id>/image/?page&zoom&rotate'},
]
