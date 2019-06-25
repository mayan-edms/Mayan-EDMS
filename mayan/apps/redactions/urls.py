from __future__ import unicode_literals

from django.conf.urls import url

from .views import (
    RedactionCreateView, RedactionEditView, RedactionListView,
)


urlpatterns = [
    url(
        regex=r'^document_pages/(?P<pk>\d+)/redactions/create/$',
        view=RedactionCreateView.as_view(), name='redaction_create'
    ),
    url(
        regex=r'^document_pages/(?P<pk>\d+)/redactions/$',
        view=RedactionListView.as_view(), name='redaction_list'
    ),
    #url(
    #    regex=r'^delete/(?P<pk>\d+)/$', view=RedactionDeleteView.as_view(),
    #    name='redaction_delete'
    #),
    url(
        regex=r'^edit/(?P<pk>\d+)/$', view=RedactionEditView.as_view(),
        name='redaction_edit'
    ),
]
api_urls = []
