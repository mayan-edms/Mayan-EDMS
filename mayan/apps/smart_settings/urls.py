from __future__ import unicode_literals

from django.conf.urls import url

from .views import NamespaceDetailView, NamespaceListView, SettingEditView

urlpatterns = [
    url(
        regex=r'^namespaces/$', view=NamespaceListView.as_view(),
        name='namespace_list'
    ),
    url(
        regex=r'^namespaces/(?P<namespace_name>\w+)/$',
        view=NamespaceDetailView.as_view(), name='namespace_detail'
    ),
    url(
        regex=r'^namespaces/settings/(?P<setting_global_name>\w+)/edit/$',
        view=SettingEditView.as_view(), name='setting_edit_view'
    ),
]
