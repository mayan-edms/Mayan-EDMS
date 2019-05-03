from __future__ import unicode_literals

from django.conf.urls import url

from .views import (
    CheckVersionView, DependencyGroupEntryListView,
    DependencyGroupEntryDetailView, DependencyGroupListView,
    DependencyLicensesView
)

urlpatterns = [
    url(
        regex=r'^check_version/$', view=CheckVersionView.as_view(),
        name='check_version_view'
    ),
    url(
        regex=r'^groups/(?P<dependency_group_name>\w+)/(?P<dependency_group_entry_name>\w+)$',
        view=DependencyGroupEntryDetailView.as_view(),
        name='dependency_group_entry_detail'
    ),
    url(
        regex=r'^groups/(?P<dependency_group_name>\w+)/$',
        view=DependencyGroupEntryListView.as_view(),
        name='dependency_group_entry_list'
    ),
    url(
        regex=r'^groups/$', view=DependencyGroupListView.as_view(),
        name='dependency_group_list'
    ),
    url(
        regex=r'^licenses/$', view=DependencyLicensesView.as_view(),
        name='dependency_licenses_view'
    ),
]
