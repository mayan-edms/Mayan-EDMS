from __future__ import unicode_literals

from django.conf.urls import url

from .api_views import (
    APIResolvedSmartLinkView, APIResolvedSmartLinkDocumentListView,
    APIResolvedSmartLinkListView, APISmartLinkListView, APISmartLinkView,
    APISmartLinkConditionListView, APISmartLinkConditionView
)
from .views import (
    DocumentSmartLinkListView, DocumentTypeSmartLinksView,
    ResolvedSmartLinkView, SetupSmartLinkDocumentTypesView,
    SmartLinkConditionListView, SmartLinkConditionCreateView,
    SmartLinkConditionEditView, SmartLinkConditionDeleteView,
    SmartLinkCreateView, SmartLinkDeleteView, SmartLinkEditView,
    SmartLinkListView
)

urlpatterns = [
    url(
        regex=r'^documents/(?P<pk>\d+)/smart_links/$',
        view=DocumentSmartLinkListView.as_view(),
        name='smart_link_instances_for_document'
    ),
    url(
        regex=r'^documents/(?P<document_pk>\d+)/smart_links/(?P<smart_link_pk>\d+)/$',
        view=ResolvedSmartLinkView.as_view(), name='smart_link_instance_view'
    ),
    url(
        regex=r'^document_types/(?P<pk>\d+)/smart_links/$',
        view=DocumentTypeSmartLinksView.as_view(),
        name='document_type_smart_links'
    ),
    url(
        regex=r'^smart_links/$', view=SmartLinkListView.as_view(),
        name='smart_link_list'
    ),
    url(
        regex=r'^smart_links/create/$', view=SmartLinkCreateView.as_view(),
        name='smart_link_create'
    ),
    url(
        regex=r'^smart_links/(?P<pk>\d+)/delete/$',
        view=SmartLinkDeleteView.as_view(), name='smart_link_delete'
    ),
    url(
        regex=r'^smart_links/(?P<pk>\d+)/edit/$', view=SmartLinkEditView.as_view(),
        name='smart_link_edit'
    ),
    url(
        regex=r'^smart_links/(?P<pk>\d+)/document_types/$',
        view=SetupSmartLinkDocumentTypesView.as_view(),
        name='smart_link_document_types'
    ),
    url(
        regex=r'^smart_links/(?P<pk>\d+)/conditions/$',
        view=SmartLinkConditionListView.as_view(),
        name='smart_link_condition_list'
    ),
    url(
        regex=r'^smart_links/(?P<pk>\d+)/conditions/create/$',
        view=SmartLinkConditionCreateView.as_view(),
        name='smart_link_condition_create'
    ),
    url(
        regex=r'^smart_links/conditions/(?P<pk>\d+)/delete/$',
        view=SmartLinkConditionDeleteView.as_view(),
        name='smart_link_condition_delete'
    ),
    url(
        regex=r'^smart_links/conditions/(?P<pk>\d+)/edit/$',
        view=SmartLinkConditionEditView.as_view(),
        name='smart_link_condition_edit'
    ),
]

api_urls = [
    url(
        regex=r'^smart_links/$', view=APISmartLinkListView.as_view(),
        name='smartlink-list'
    ),
    url(
        regex=r'^smart_links/(?P<pk>[0-9]+)/$',
        view=APISmartLinkView.as_view(), name='smartlink-detail'
    ),
    url(
        regex=r'^smart_links/(?P<pk>[0-9]+)/conditions/$',
        view=APISmartLinkConditionListView.as_view(),
        name='smartlinkcondition-list'
    ),
    url(
        regex=r'^smart_links/(?P<pk>[0-9]+)/conditions/(?P<condition_pk>[0-9]+)/$',
        view=APISmartLinkConditionView.as_view(),
        name='smartlinkcondition-detail'
    ),
    url(
        regex=r'^documents/(?P<pk>[0-9]+)/resolved_smart_links/$',
        view=APIResolvedSmartLinkListView.as_view(),
        name='resolvedsmartlink-list'
    ),
    url(
        regex=r'^documents/(?P<pk>[0-9]+)/resolved_smart_links/(?P<smart_link_pk>[0-9]+)/$',
        view=APIResolvedSmartLinkView.as_view(),
        name='resolvedsmartlink-detail'
    ),
    url(
        regex=r'^documents/(?P<pk>[0-9]+)/resolved_smart_links/(?P<smart_link_pk>[0-9]+)/documents/$',
        view=APIResolvedSmartLinkDocumentListView.as_view(),
        name='resolvedsmartlinkdocument-list'
    ),
]
