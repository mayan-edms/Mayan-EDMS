from django.conf.urls import url

from .views import (
    SettingEditView, SettingNamespaceDetailView, SettingNamespaceListView
)

urlpatterns = [
    url(
        regex=r'^namespaces/settings/(?P<setting_global_name>\w+)/edit/$',
        name='setting_edit_view', view=SettingEditView.as_view()
    ),
    url(
        regex=r'^namespaces/$', name='namespace_list',
        view=SettingNamespaceListView.as_view()
    ),
    url(
        regex=r'^namespaces/(?P<namespace_name>\w+)/$',
        name='namespace_detail', view=SettingNamespaceDetailView.as_view()
    )
]
