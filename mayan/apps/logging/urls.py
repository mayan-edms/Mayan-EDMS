from django.conf.urls import url

from .views import (
    ObjectErrorLogEntryListClearView, ObjectErrorLogEntryListView,
)

urlpatterns = [
    url(
        regex=r'^object/(?P<app_label>[-\w]+)/(?P<model_name>[-\w]+)/(?P<object_id>\d+)/errors/$',
        name='object_error_list', view=ObjectErrorLogEntryListView.as_view()
    ),
    url(
        regex=r'^object/(?P<app_label>[-\w]+)/(?P<model_name>[-\w]+)/(?P<object_id>\d+)/errors/clear/$',
        name='object_error_list_clear',
        view=ObjectErrorLogEntryListClearView.as_view()
    )
]
