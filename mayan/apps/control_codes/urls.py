from __future__ import unicode_literals

from django.conf.urls import url

from .api_views import (
    APIControlSheetCodeListView, APIControlSheetCodeView,
    APIControlSheetListView, APIControlSheetView,
    APIControlSheetCodeImageView
)
from .views import ControlSheetDetailView

urlpatterns = [
    url(
        regex=r'^control_sheets/(?P<control_sheet_id>\d+)/$',
        view=ControlSheetDetailView.as_view(), name='control_sheet_detail'
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
