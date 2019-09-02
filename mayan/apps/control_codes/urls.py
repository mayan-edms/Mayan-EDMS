from __future__ import unicode_literals

from django.conf.urls import url

from .api_views import (
    APIControlSheetCodeListView, APIControlSheetCodeView,
    APIControlSheetListView, APIControlSheetView,
    APIControlSheetCodeImageView
)
from .views import (
    ControlSheetCreateView, ControlSheetDeleteView, ControlSheetEditView,
    ControlSheetListView, ControlSheetPreviewView
)

urlpatterns = [
    url(
        regex=r'^control_sheets/$',
        view=ControlSheetListView.as_view(), name='control_sheet_list'
    ),
    url(
        regex=r'^control_sheets/create/$',
        view=ControlSheetCreateView.as_view(), name='control_sheet_create'
    ),
    url(
        regex=r'^control_sheets/(?P<control_sheet_id>\d+)/delete/$',
        view=ControlSheetDeleteView.as_view(), name='control_sheet_delete'
    ),
    url(
        regex=r'^control_sheets/(?P<control_sheet_id>\d+)/edit/$',
        view=ControlSheetEditView.as_view(), name='control_sheet_edit'
    ),
    url(
        regex=r'^control_sheets/(?P<control_sheet_id>\d+)/preview/$',
        view=ControlSheetPreviewView.as_view(), name='control_sheet_preview'
    ),
]

api_urls = [
    url(
        regex=r'^control_sheets/$', view=APIControlSheetListView.as_view(),
        name='controlsheet-list'
    ),
    url(
        regex=r'^control_sheets/(?P<control_sheet_id>[0-9]+)/$',
        view=APIControlSheetView.as_view(),
        name='controlsheet-detail'
    ),
    url(
        regex=r'^control_sheets/(?P<control_sheet_id>[0-9]+)/codes/$',
        view=APIControlSheetCodeListView.as_view(), name='controlsheet-code-list'
    ),
    url(
        regex=r'^control_sheets/(?P<control_sheet_id>[0-9]+)/codes/(?P<control_sheet_code_id>[0-9]+)/$',
        view=APIControlSheetCodeView.as_view(), name='controlsheet-code-detail'
    ),
    url(
        regex=r'^control_sheets/(?P<control_sheet_id>[0-9]+)/codes/(?P<control_sheet_code_id>[0-9]+)/image/$',
        name='controlsheet-code-image', view=APIControlSheetCodeImageView.as_view()
    ),
]
