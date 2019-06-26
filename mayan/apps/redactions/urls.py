from __future__ import unicode_literals

from django.conf.urls import url

from .views import (
    RedactionCreateView, RedactionDeleteView, RedactionEditView,
    RedactionListView,
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
    url(
        regex=r'^redactions/(?P<pk>\d+)/delete/$',
        view=RedactionDeleteView.as_view(), name='redaction_delete'
    ),
    url(
        regex=r'^redactions/(?P<pk>\d+)/edit/$',
        view=RedactionEditView.as_view(), name='redaction_edit'
    ),
]

api_urls = []
