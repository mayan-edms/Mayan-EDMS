from __future__ import unicode_literals

from django.conf.urls import patterns, url
from django.views.generic import TemplateView


urlpatterns = patterns('common.views',
    url(r'^about/$', TemplateView.as_view(template_name='main/about.html'), name='about_view'),
    url(r'^license/$', 'license_view', (), name='license_view'),
    url(r'^password/change/done/$', 'password_change_done', (), name='password_change_done'),
    url(r'^object/multiple/action/$', 'multi_object_action_view', (), name='multi_object_action_view'),

    url(r'^user/$', 'current_user_details', (), name='current_user_details'),
    url(r'^user/edit/$', 'current_user_edit', (), name='current_user_edit'),

    url(r'^user/locale/$', 'current_user_locale_profile_details', (), name='current_user_locale_profile_details'),
    url(r'^user/locale/edit/$', 'current_user_locale_profile_edit', (), name='current_user_locale_profile_edit'),

    url(r'^login/$', 'login_view', (), name='login_view'),
    url(r'^password/change/$', 'password_change_view', (), name='password_change_view'),
)

urlpatterns += patterns('',
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': 'main:home'}, name='logout_view'),

    url(r'^password/reset/$', 'django.contrib.auth.views.password_reset', {'email_template_name': 'main/password_reset_email.html', 'template_name': 'main/password_reset_form.html', 'post_reset_redirect': '/password/reset/done'}, name='password_reset_view'),
    url(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', {'template_name': 'main/password_reset_confirm.html', 'post_reset_redirect': '/password/reset/complete/'}, name='password_reset_confirm_view'),
    url(r'^password/reset/complete/$', 'django.contrib.auth.views.password_reset_complete', {'template_name': 'main/password_reset_complete.html'}, name='password_reset_complete_view'),
    url(r'^password/reset/done/$', 'django.contrib.auth.views.password_reset_done', {'template_name': 'main/password_reset_done.html'}, name='password_reset_done_view'),
)

urlpatterns += patterns('',
    url(r'^set_language/$', 'django.views.i18n.set_language', name='set_language'),
)
