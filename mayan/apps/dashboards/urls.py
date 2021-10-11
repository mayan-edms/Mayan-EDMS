from django.conf.urls import url

from .views import DashboardDetailView, DashboardListView

urlpatterns = [
    url(
        regex=r'^dashboards/$', name='dashboard_list',
        view=DashboardListView.as_view()
    ),
    url(
        regex=r'^dashboards/(?P<dashboard_name>[-\w]+)/$',
        name='dashboard_detail', view=DashboardDetailView.as_view()
    ),
]
