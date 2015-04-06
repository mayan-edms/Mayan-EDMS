from __future__ import unicode_literals

from django.conf.urls import patterns, url
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.views.generic import RedirectView

from .views import AboutView


urlpatterns = patterns('common.views',
    url(r'^$', 'home', (), 'home'),
    url(r'^maintenance_menu/$', 'maintenance_menu', (), 'maintenance_menu'),

    url(r'^about/$', AboutView.as_view(), name='about_view'),
    url(r'^license/$', 'license_view', (), name='license_view'),
    url(r'^object/multiple/action/$', 'multi_object_action_view', (), name='multi_object_action_view'),

    url(r'^user/$', 'current_user_details', (), name='current_user_details'),
    url(r'^user/edit/$', 'current_user_edit', (), name='current_user_edit'),

    url(r'^user/locale/$', 'current_user_locale_profile_details', (), name='current_user_locale_profile_details'),
    url(r'^user/locale/edit/$', 'current_user_locale_profile_edit', (), name='current_user_locale_profile_edit'),

    url(r'^setup/$', 'setup_list', (), 'setup_list'),
    url(r'^tools/$', 'tools_list', (), 'tools_list'),
)

urlpatterns += patterns('',
    url(r'^set_language/$', 'django.views.i18n.set_language', name='set_language'),
    (r'^favicon\.ico$', RedirectView.as_view(url=static('appearance/images/favicon.ico'))),
)
