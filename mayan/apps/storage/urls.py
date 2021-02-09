from django.conf.urls import url

from .views import (
    DownloadFileDeleteView, DownloadFileDownloadViewView,
    DownloadFileListView
)

urlpatterns = [
    url(
        regex=r'^downloads/(?P<download_file_id>\d+)/delete/$',
        name='download_file_delete',
        view=DownloadFileDeleteView.as_view()
    ),
    url(
        regex=r'^downloads/(?P<download_file_id>\d+)/download/$',
        name='download_file_download',
        view=DownloadFileDownloadViewView.as_view()
    ),
    url(
        regex=r'^downloads/$', name='download_file_list',
        view=DownloadFileListView.as_view()
    ),
]
