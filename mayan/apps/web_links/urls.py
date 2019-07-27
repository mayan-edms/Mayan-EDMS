from __future__ import unicode_literals

from django.conf.urls import url

from .views import (
    DocumentWebLinkListView, DocumentTypeWebLinksView, ResolvedWebLinkView,
    WebLinkCreateView, WebLinkDeleteView, WebLinkDocumentTypesView,
    WebLinkEditView, WebLinkListView
)

urlpatterns = [
    url(
        regex=r'^document_types/(?P<pk>\d+)/web_links/$',
        view=DocumentTypeWebLinksView.as_view(),
        name='document_type_web_links'
    ),
    url(
        regex=r'^documents/(?P<pk>\d+)/web_links/$',
        view=DocumentWebLinkListView.as_view(),
        name='document_web_link_list'
    ),
    url(
        regex=r'^documents/(?P<document_pk>\d+)/(?P<web_link_pk>\d+)/$',
        view=ResolvedWebLinkView.as_view(), name='web_link_instance_view'
    ),
    url(
        regex=r'^weblinks/$', view=WebLinkListView.as_view(),
        name='web_link_list'
    ),
    url(
        regex=r'^weblinks/create/$', view=WebLinkCreateView.as_view(),
        name='web_link_create'
    ),
    url(
        regex=r'^weblinks/(?P<pk>\d+)/delete/$',
        view=WebLinkDeleteView.as_view(), name='web_link_delete'
    ),
    url(
        regex=r'^weblinks/(?P<pk>\d+)/document_types/$',
        view=WebLinkDocumentTypesView.as_view(),
        name='web_link_document_types'
    ),
    url(
        regex=r'^weblinks/(?P<pk>\d+)/edit/$', view=WebLinkEditView.as_view(),
        name='web_link_edit'
    ),
]
