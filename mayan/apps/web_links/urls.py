from django.conf.urls import url

from .api_views import (
    APIResolvedWebLinkListView, APIResolvedWebLinkNavigateView,
    APIResolvedWebLinkView, APIWebLinkDocumentTypeAddView,
    APIWebLinkDocumentTypeListView, APIWebLinkDocumentTypeRemoveView,
    APIWebLinkView, APIWebLinkListView
)
from .views import (
    DocumentWebLinkListView, DocumentTypeWebLinksView, ResolvedWebLinkView,
    WebLinkCreateView, WebLinkDeleteView, WebLinkDocumentTypesView,
    WebLinkEditView, WebLinkListView
)

urlpatterns = [
    url(
        regex=r'^document_types/(?P<document_type_id>\d+)/web_links/$',
        name='document_type_web_links',
        view=DocumentTypeWebLinksView.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_id>\d+)/web_links/$',
        name='document_web_link_list', view=DocumentWebLinkListView.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_id>\d+)/web_links/(?P<web_link_id>\d+)/$',
        name='web_link_instance_view', view=ResolvedWebLinkView.as_view()
    ),
    url(
        regex=r'^weblinks/$', name='web_link_list',
        view=WebLinkListView.as_view()
    ),
    url(
        regex=r'^weblinks/create/$', name='web_link_create',
        view=WebLinkCreateView.as_view()
    ),
    url(
        regex=r'^weblinks/(?P<web_link_id>\d+)/delete/$',
        name='web_link_delete', view=WebLinkDeleteView.as_view()
    ),
    url(
        regex=r'^weblinks/(?P<web_link_id>\d+)/document_types/$',
        name='web_link_document_types',
        view=WebLinkDocumentTypesView.as_view()
    ),
    url(
        regex=r'^weblinks/(?P<web_link_id>\d+)/edit/$', name='web_link_edit',
        view=WebLinkEditView.as_view()
    )
]

api_urls = [
    url(
        regex=r'^documents/(?P<document_id>[0-9]+)/resolved_web_links/$',
        name='resolved_web_link-list',
        view=APIResolvedWebLinkListView.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_id>[0-9]+)/resolved_web_links/(?P<resolved_web_link_id>[0-9]+)/$',
        name='resolved_web_link-detail',
        view=APIResolvedWebLinkView.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_id>[0-9]+)/resolved_web_links/(?P<resolved_web_link_id>[0-9]+)/navigate/$',
        name='resolved_web_link-navigate',
        view=APIResolvedWebLinkNavigateView.as_view()
    ),
    url(
        regex=r'^web_links/$', name='web_link-list',
        view=APIWebLinkListView.as_view()
    ),
    url(
        regex=r'^web_links/(?P<web_link_id>[0-9]+)/$',
        name='web_link-detail', view=APIWebLinkView.as_view()
    ),
    url(
        regex=r'^web_links/(?P<web_link_id>[0-9]+)/document_types/$',
        name='web_link-document_type-list',
        view=APIWebLinkDocumentTypeListView.as_view()
    ),
    url(
        regex=r'^web_links/(?P<web_link_id>[0-9]+)/document_types/add/$',
        name='web_link-document_type-add',
        view=APIWebLinkDocumentTypeAddView.as_view()
    ),
    url(
        regex=r'^web_links/(?P<web_link_id>[0-9]+)/document_types/remove/$',
        name='web_link-document_type-remove',
        view=APIWebLinkDocumentTypeRemoveView.as_view()
    ),
]
