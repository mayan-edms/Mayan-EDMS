from __future__ import unicode_literals

from django.conf.urls import url
from django.views.i18n import javascript_catalog, set_language

from .api_views import APIContentTypeList
from .views import (
    AboutView, CheckVersionView, CurrentUserDetailsView, CurrentUserEditView,
    CurrentUserLocaleProfileDetailsView, CurrentUserLocaleProfileEditView,
    FaviconRedirectView, HomeView, LicenseView, ObjectErrorLogEntryListClearView,
    ObjectErrorLogEntryListView, PackagesLicensesView, RootView, SetupListView,
    ToolsListView, multi_object_action_view
)

urlpatterns = [
    url(r'^$', RootView.as_view(), name='root'),
    url(r'^home/$', HomeView.as_view(), name='home'),
    url(r'^about/$', AboutView.as_view(), name='about_view'),
    url(
        r'^check_version/$', CheckVersionView.as_view(),
        name='check_version_view'
    ),
    url(r'^license/$', LicenseView.as_view(), name='license_view'),
    url(
        r'^packages/licenses/$', PackagesLicensesView.as_view(),
        name='packages_licenses_view'
    ),
    url(
        r'^object/multiple/action/$', multi_object_action_view,
        name='multi_object_action_view'
    ),
    url(r'^setup/$', SetupListView.as_view(), name='setup_list'),
    url(r'^tools/$', ToolsListView.as_view(), name='tools_list'),
    url(
        r'^user/$', CurrentUserDetailsView.as_view(),
        name='current_user_details'
    ),
    url(
        r'^user/edit/$', CurrentUserEditView.as_view(),
        name='current_user_edit'
    ),
    url(
        r'^user/locale/$', CurrentUserLocaleProfileDetailsView.as_view(),
        name='current_user_locale_profile_details'
    ),
    url(
        r'^user/locale/edit/$', CurrentUserLocaleProfileEditView.as_view(),
        name='current_user_locale_profile_edit'
    ),
    url(
        r'^object/(?P<app_label>[-\w]+)/(?P<model>[-\w]+)/(?P<object_id>\d+)/errors/$',
        ObjectErrorLogEntryListView.as_view(), name='object_error_list'
    ),
    url(
        r'^object/(?P<app_label>[-\w]+)/(?P<model>[-\w]+)/(?P<object_id>\d+)/errors/clear/$',
        ObjectErrorLogEntryListClearView.as_view(),
        name='object_error_list_clear'
    ),
]

urlpatterns += [
    url(
        r'^favicon\.ico$', FaviconRedirectView.as_view()
    ),
    url(
        r'^jsi18n/(?P<packages>\S+?)/$', javascript_catalog,
        name='javascript_catalog'
    ),
    url(
        r'^set_language/$', set_language, name='set_language'
    ),
]

api_urls = [
    url(
        r'^content_types/$', APIContentTypeList.as_view(),
        name='content-type-list'
    ),
]
