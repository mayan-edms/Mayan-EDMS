from django.conf.urls import url

from .views import NamespaceDetailView, NamespaceListView, SettingEditView

urlpatterns = [
    url(
        regex=r'^namespaces/$', name='namespace_list',
        view=NamespaceListView.as_view()
    ),
    url(
        regex=r'^namespaces/(?P<namespace_name>\w+)/$',
        name='namespace_detail', view=NamespaceDetailView.as_view()
    ),
    url(
        regex=r'^namespaces/settings/(?P<setting_global_name>\w+)/edit/$',
        name='setting_edit_view', view=SettingEditView.as_view()
    ),
]
