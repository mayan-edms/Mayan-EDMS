from __future__ import unicode_literals

from django.conf.urls import url

from .views import (
    DocumentSmartLinkListView, ResolvedSmartLinkView,
    SetupSmartLinkDocumentTypesView, SmartLinkConditionListView,
    SmartLinkConditionCreateView, SmartLinkConditionEditView,
    SmartLinkConditionDeleteView, SmartLinkCreateView, SmartLinkDeleteView,
    SmartLinkEditView, SmartLinkListView
)

urlpatterns = [
    url(
        r'^document/(?P<pk>\d+)/list/$', DocumentSmartLinkListView.as_view(),
        name='smart_link_instances_for_document'
    ),
    url(
        r'^document/(?P<document_pk>\d+)/(?P<smart_link_pk>\d+)/$',
        ResolvedSmartLinkView.as_view(), name='smart_link_instance_view'
    ),

    url(
        r'^setup/list/$', SmartLinkListView.as_view(), name='smart_link_list'
    ),
    url(
        r'^setup/create/$', SmartLinkCreateView.as_view(),
        name='smart_link_create'
    ),
    url(
        r'^setup/(?P<pk>\d+)/delete/$',
        SmartLinkDeleteView.as_view(), name='smart_link_delete'
    ),
    url(
        r'^setup/(?P<pk>\d+)/edit/$', SmartLinkEditView.as_view(),
        name='smart_link_edit'
    ),
    url(
        r'^setup/(?P<pk>\d+)/document_types/$',
        SetupSmartLinkDocumentTypesView.as_view(),
        name='smart_link_document_types'
    ),

    url(
        r'^setup/(?P<pk>\d+)/condition/list/$',
        SmartLinkConditionListView.as_view(), name='smart_link_condition_list'
    ),
    url(
        r'^setup/(?P<pk>\d+)/condition/create/$',
        SmartLinkConditionCreateView.as_view(),
        name='smart_link_condition_create'
    ),
    url(
        r'^setup/smart_link/condition/(?P<pk>\d+)/edit/$',
        SmartLinkConditionEditView.as_view(), name='smart_link_condition_edit'
    ),
    url(
        r'^setup/smart_link/condition/(?P<pk>\d+)/delete/$',
        SmartLinkConditionDeleteView.as_view(),
        name='smart_link_condition_delete'
    ),
]
