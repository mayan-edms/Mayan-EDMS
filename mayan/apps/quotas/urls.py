from __future__ import unicode_literals

from django.conf.urls import url

from .views import (
    QuotaBackendSelectionView, QuotaCreateView, QuotaDeleteView,
    QuotaEditView, QuotaListView
)

urlpatterns = [
    url(
        r'^quotas/backend/selection/$',
        QuotaBackendSelectionView.as_view(),
        name='quota_backend_selection'
    ),
    url(
        r'^quotas/(?P<class_path>[a-zA-Z0-9_.]+)/create/$',
        QuotaCreateView.as_view(), name='quota_create'
    ),
    url(
        r'^quotas/(?P<pk>\d+)/delete/$', QuotaDeleteView.as_view(),
        name='quota_delete'
    ),
    url(
        r'^quotas/(?P<pk>\d+)/edit/$', QuotaEditView.as_view(),
        name='quota_edit'
    ),
    url(
        r'^quotas/$', QuotaListView.as_view(),
        name='quota_list'
    ),
]
