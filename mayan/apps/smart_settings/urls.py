from __future__ import unicode_literals

from django.conf.urls import url

from .views import NamespaceDetailView, NamespaceListView, SettingEditView

urlpatterns = [
    url(
        regex=r'^namespace/all/$', view=NamespaceListView.as_view(),
        name='namespace_list'
    ),
    url(
        regex=r'^namespace/(?P<namespace_name>\w+)/$',
        view=NamespaceDetailView.as_view(), name='namespace_detail'
    ),
    url(
        regex=r'^edit/(?P<setting_global_name>\w+)/$',
        view=SettingEditView.as_view(), name='setting_edit_view'
    ),
]
