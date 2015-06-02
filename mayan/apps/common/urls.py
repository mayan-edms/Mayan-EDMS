from __future__ import unicode_literals

from django.conf.urls import patterns, url
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.views.generic import RedirectView

from .views import (
    AboutView, CurrentUserDetailsView, CurrentUserLocaleProfileDetailsView,
    HomeView, LicenseView, MaintenanceMenuView, SetupListView, ToolsListView
)

urlpatterns = patterns(
    'common.views',
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^about/$', AboutView.as_view(), name='about_view'),
    url(r'^license/$', LicenseView.as_view(), name='license_view'),
    url(r'^maintenance_menu/$', MaintenanceMenuView.as_view(), name='maintenance_menu'),
    url(r'^object/multiple/action/$', 'multi_object_action_view', name='multi_object_action_view'),
    url(r'^setup/$', SetupListView.as_view(), name='setup_list'),
    url(r'^tools/$', ToolsListView.as_view(), name='tools_list'),
    url(r'^user/$', CurrentUserDetailsView.as_view(), name='current_user_details'),
    url(r'^user/edit/$', 'current_user_edit', name='current_user_edit'),
    url(r'^user/locale/$', CurrentUserLocaleProfileDetailsView.as_view(), name='current_user_locale_profile_details'),
    url(r'^user/locale/edit/$', 'current_user_locale_profile_edit', name='current_user_locale_profile_edit'),
)

urlpatterns += patterns(
    '',
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': 'main:home'}, name='logout_view'),

    url(r'^password/reset/$', 'django.contrib.auth.views.password_reset', {'email_template_name': 'main/password_reset_email.html', 'template_name': 'main/password_reset_form.html', 'post_reset_redirect': '/password/reset/done'}, name='password_reset_view'),
    url(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', {'template_name': 'main/password_reset_confirm.html', 'post_reset_redirect': '/password/reset/complete/'}, name='password_reset_confirm_view'),
    url(r'^password/reset/complete/$', 'django.contrib.auth.views.password_reset_complete', {'template_name': 'main/password_reset_complete.html'}, name='password_reset_complete_view'),
    url(r'^password/reset/done/$', 'django.contrib.auth.views.password_reset_done', {'template_name': 'main/password_reset_done.html'}, name='password_reset_done_view'),
)

urlpatterns += patterns(
    '',
    url(r'^set_language/$', 'django.views.i18n.set_language', name='set_language'),
    (r'^favicon\.ico$', RedirectView.as_view(url=static('appearance/images/favicon.ico'))),
)
