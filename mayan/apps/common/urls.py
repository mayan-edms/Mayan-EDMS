from __future__ import unicode_literals

from django.conf.urls import url
from django.views.i18n import javascript_catalog, set_language

from .api_views import (
    APIContentTypeList, APITemplateDetailView, APITemplateListView
)
from .views import (
    AboutView, CheckVersionView, CurrentUserDetailsView, CurrentUserEditView,
    CurrentUserLocaleProfileDetailsView, CurrentUserLocaleProfileEditView,
    FaviconRedirectView, HomeView, LicenseView,
    ObjectErrorLogEntryListClearView, ObjectErrorLogEntryListView,
    PackagesLicensesView, RootView, SetupListView, ToolsListView,
    multi_object_action_view
)

urlpatterns = [
    url(regex=r'^$', view=RootView.as_view(), name='root'),
    url(regex=r'^home/$', view=HomeView.as_view(), name='home'),
    url(regex=r'^about/$', view=AboutView.as_view(), name='about_view'),
    url(
        regex=r'^check_version/$', view=CheckVersionView.as_view(),
        name='check_version_view'
    ),
    url(regex=r'^license/$', view=LicenseView.as_view(), name='license_view'),
    url(
        regex=r'^packages/licenses/$', view=PackagesLicensesView.as_view(),
        name='packages_licenses_view'
    ),
    url(
        regex=r'^object/multiple/action/$', view=multi_object_action_view,
        name='multi_object_action_view'
    ),
    url(regex=r'^setup/$', view=SetupListView.as_view(), name='setup_list'),
    url(regex=r'^tools/$', view=ToolsListView.as_view(), name='tools_list'),
    url(
        regex=r'^user/$', view=CurrentUserDetailsView.as_view(),
        name='current_user_details'
    ),
    url(
        regex=r'^user/edit/$', view=CurrentUserEditView.as_view(),
        name='current_user_edit'
    ),
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

urlpatterns += [
    url(
        regex=r'^favicon\.ico$', view=FaviconRedirectView.as_view()
    ),
    url(
        regex=r'^jsi18n/(?P<packages>\S+?)/$', view=javascript_catalog,
        name='javascript_catalog'
    ),
    url(
        regex=r'^set_language/$', view=set_language, name='set_language'
    ),
]

api_urls = [
    url(
        regex=r'^content_types/$', view=APIContentTypeList.as_view(),
        name='content-type-list'
    ),
    url(
        regex=r'^templates/$', view=APITemplateListView.as_view(),
        name='template-list'
    ),
    url(
        regex=r'^templates/(?P<name>[-\w]+)/$',
        view=APITemplateDetailView.as_view(), name='template-detail'
    ),
]
