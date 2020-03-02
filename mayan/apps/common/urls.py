from __future__ import unicode_literals

from django.conf.urls import url
from django.views.i18n import JavaScriptCatalog

from .api_views import ContentTypeAPIViewSet, TemplateAPIViewSet
from .views import (
    AboutView, CurrentUserLocaleProfileDetailsView,
    CurrentUserLocaleProfileEditView, FaviconRedirectView, HomeView,
    LicenseView, ObjectErrorLogEntryListClearView, ObjectErrorLogEntryListView,
    RootView, SetupListView, ToolsListView
)

urlpatterns_error_logs = [
    url(
        regex=r'^object/(?P<app_label>[-\w]+)/(?P<model>[-\w]+)/(?P<object_id>\d+)/errors/$',
        view=ObjectErrorLogEntryListView.as_view(), name='object_error_list'
    ),
    url(
        regex=r'^object/(?P<app_label>[-\w]+)/(?P<model>[-\w]+)/(?P<object_id>\d+)/errors/clear/$',
        view=ObjectErrorLogEntryListClearView.as_view(),
        name='object_error_list_clear'
    ),
]

urlpatterns_user_locale = [
    url(
        regex=r'^user/locale/$',
        view=CurrentUserLocaleProfileDetailsView.as_view(),
        name='current_user_locale_profile_details'
    ),
    url(
        regex=r'^user/locale/edit/$',
        view=CurrentUserLocaleProfileEditView.as_view(),
        name='current_user_locale_profile_edit'
    ),
]

urlpatterns_misc = [
    url(
        regex=r'^favicon\.ico$', view=FaviconRedirectView.as_view()
    ),
    url(
        regex=r'^jsi18n/(?P<packages>\S+?)/$', view=JavaScriptCatalog.as_view(),
        name='javascript_catalog'
    ),
]

urlpatterns = [
    url(regex=r'^$', view=RootView.as_view(), name='root'),
    url(regex=r'^home/$', view=HomeView.as_view(), name='home'),
    url(regex=r'^about/$', view=AboutView.as_view(), name='about_view'),
    url(regex=r'^license/$', view=LicenseView.as_view(), name='license_view'),
    url(regex=r'^setup/$', view=SetupListView.as_view(), name='setup_list'),
    url(regex=r'^tools/$', view=ToolsListView.as_view(), name='tools_list'),
]

urlpatterns.extend(urlpatterns_error_logs)
urlpatterns.extend(urlpatterns_misc)
urlpatterns.extend(urlpatterns_user_locale)

api_router_entries = (
    {
        'prefix': r'content_types', 'viewset': ContentTypeAPIViewSet,
        'basename': 'content_type'
    },
    {
        'prefix': r'templates', 'viewset': TemplateAPIViewSet,
        'basename': 'template'
    },
)
