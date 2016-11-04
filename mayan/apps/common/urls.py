from __future__ import unicode_literals

from django.conf.urls import url
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.views.generic import RedirectView
from django.views.i18n import javascript_catalog, set_language

from .views import (
    AboutView, CurrentUserDetailsView, CurrentUserEditView,
    CurrentUserLocaleProfileDetailsView, CurrentUserLocaleProfileEditView,
    FilterResultListView, FilterSelectView, HomeView, LicenseView,
    PackagesLicensesView, SetupListView, ToolsListView,
    multi_object_action_view
)

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^about/$', AboutView.as_view(), name='about_view'),
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
        r'^filter/select/$', FilterSelectView.as_view(),
        name='filter_selection'
    ),
    url(
        r'^filter/(?P<slug>[\w-]+)/results/$', FilterResultListView.as_view(),
        name='filter_results'
    ),
]

urlpatterns += [
    url(
        r'^favicon\.ico$', RedirectView.as_view(
            permanent=True, url=static('appearance/images/favicon.ico')
        )
    ),
    url(
        r'^jsi18n/(?P<packages>\S+?)/$', javascript_catalog,
        name='javascript_catalog'
    ),
    url(
        r'^set_language/$', set_language, name='set_language'
    ),
]
