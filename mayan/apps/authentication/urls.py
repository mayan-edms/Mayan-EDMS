from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import patterns, url

urlpatterns = patterns(
    'authentication.views',
    url(r'^login/$', 'login_view', name='login_view'),
    url(
        r'^password/change/done/$', 'password_change_done',
        name='password_change_done'
    ),
    url(
        r'^password/change/$', 'password_change_view',
        name='password_change_view'
    ),
)

urlpatterns += patterns(
    '',
    url(
        r'^logout/$', 'django.contrib.auth.views.logout',
        {'next_page': settings.LOGIN_REDIRECT_URL}, name='logout_view'
    ),
    url(
        r'^password/reset/$', 'django.contrib.auth.views.password_reset',
        {
            'email_template_name': 'appearance/password_reset_email.html',
            'template_name': 'appearance/password_reset_form.html',
            'post_reset_redirect': '/password/reset/done'
        }, name='password_reset_view'
    ),
    url(
        r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        'django.contrib.auth.views.password_reset_confirm', {
            'template_name': 'appearance/password_reset_confirm.html',
            'post_reset_redirect': '/password/reset/complete/'
        }, name='password_reset_confirm_view'
    ),
    url(
        r'^password/reset/complete/$',
        'django.contrib.auth.views.password_reset_complete', {
            'template_name': 'appearance/password_reset_complete.html'
        }, name='password_reset_complete_view'),
    url(
        r'^password/reset/done/$',
        'django.contrib.auth.views.password_reset_done', {
            'template_name': 'appearance/password_reset_done.html'
        }, name='password_reset_done_view'),
)
