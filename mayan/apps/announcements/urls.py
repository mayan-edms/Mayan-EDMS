from django.conf.urls import url

from .api_views import APIAnnouncementListView, APIAnnouncementView
from .views import (
    AnnouncementCreateView, AnnouncementDeleteView, AnnouncementEditView, AnnouncementListView
)

urlpatterns = [
    url(
        regex=r'^announcements/$', name='announcement_list',
        view=AnnouncementListView.as_view()
    ),
    url(
        regex=r'^announcements/create/$', name='announcement_create',
        view=AnnouncementCreateView.as_view()
    ),
    url(
        regex=r'^announcements/(?P<announcement_id>\d+)/delete/$',
        name='announcement_single_delete', view=AnnouncementDeleteView.as_view()
    ),
    url(
        regex=r'^announcements/multiple/delete/$',
        name='announcement_multiple_delete', view=AnnouncementDeleteView.as_view()
    ),
    url(
        regex=r'^announcements/(?P<announcement_id>\d+)/edit/$', name='announcement_edit',
        view=AnnouncementEditView.as_view()
    ),
]

api_urls = [
    url(
        regex=r'^announcements/$', name='announcement-list',
        view=APIAnnouncementListView.as_view()
    ),
    url(
        regex=r'^announcements/(?P<announcement_id>[0-9]+)/$', name='announcement-detail',
        view=APIAnnouncementView.as_view()
    ),
]
