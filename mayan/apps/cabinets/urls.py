from __future__ import unicode_literals

from django.conf.urls import url

from .api_views import (
    APIDocumentCabinetListView, APICabinetDocumentListView,
    APICabinetDocumentView, APICabinetListView, APICabinetView
)
from .views import (
    DocumentAddToCabinetView, DocumentCabinetListView,
    DocumentRemoveFromCabinetView, CabinetChildAddView, CabinetCreateView,
    CabinetDeleteView, CabinetDetailView, CabinetEditView, CabinetListView,
)

urlpatterns = [
    url(
        regex=r'^list/$', view=CabinetListView.as_view(), name='cabinet_list'
    ),
    url(
        regex=r'^(?P<pk>\d+)/child/add/$', view=CabinetChildAddView.as_view(),
        name='cabinet_child_add'
    ),
    url(
        regex=r'^create/$', view=CabinetCreateView.as_view(),
        name='cabinet_create'
    ),
    url(
        regex=r'^(?P<pk>\d+)/edit/$', view=CabinetEditView.as_view(),
        name='cabinet_edit'
    ),
    url(
        regex=r'^(?P<pk>\d+)/delete/$', view=CabinetDeleteView.as_view(),
        name='cabinet_delete'
    ),
    url(
        regex=r'^(?P<pk>\d+)/$', view=CabinetDetailView.as_view(),
        name='cabinet_view'
    ),
    url(
        regex=r'^document/(?P<pk>\d+)/cabinet/add/$',
        view=DocumentAddToCabinetView.as_view(), name='document_cabinet_add'
    ),
    url(
        regex=r'^document/multiple/cabinet/add/$',
        view=DocumentAddToCabinetView.as_view(),
        name='document_multiple_cabinet_add'
    ),
    url(
        regex=r'^document/(?P<pk>\d+)/cabinet/remove/$',
        view=DocumentRemoveFromCabinetView.as_view(),
        name='document_cabinet_remove'
    ),
    url(
        regex=r'^document/multiple/cabinet/remove/$',
        view=DocumentRemoveFromCabinetView.as_view(),
        name='multiple_document_cabinet_remove'
    ),
    url(
        regex=r'^document/(?P<pk>\d+)/cabinet/list/$',
        view=DocumentCabinetListView.as_view(), name='document_cabinet_list'
    ),
]

api_urls = [
    url(
        regex=r'^cabinets/(?P<pk>[0-9]+)/documents/(?P<document_pk>[0-9]+)/$',
        view=APICabinetDocumentView.as_view(), name='cabinet-document'
    ),
    url(
        regex=r'^cabinets/(?P<pk>[0-9]+)/documents/$',
        view=APICabinetDocumentListView.as_view(), name='cabinet-document-list'
    ),
    url(
        regex=r'^cabinets/(?P<pk>[0-9]+)/$', view=APICabinetView.as_view(),
        name='cabinet-detail'
    ),
    url(
        regex=r'^cabinets/$', view=APICabinetListView.as_view(),
        name='cabinet-list'
    ),
    url(
        regex=r'^documents/(?P<pk>[0-9]+)/cabinets/$',
        view=APIDocumentCabinetListView.as_view(), name='document-cabinet-list'
    ),
]
