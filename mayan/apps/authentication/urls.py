from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import url
from django.contrib.auth.views import (
    logout, password_reset, password_reset_confirm, password_reset_complete,
    password_reset_done
)

from .views import login_view, password_change_done, password_change_view


urlpatterns = [
    url(r'^login/$', login_view, name='login_view'),
    url(
        r'^password/change/done/$', password_change_done,
        name='password_change_done'
    ),
    url(
        r'^password/change/$', password_change_view,
        name='password_change_view'
    ),
]

urlpatterns += [
    url(
        r'^logout/$', logout, {'next_page': settings.LOGIN_REDIRECT_URL},
        name='logout_view'
    ),
    url(
        r'^password/reset/$', password_reset, {
            'email_template_name': 'appearance/password_reset_email.html',
            'template_name': 'appearance/password_reset_form.html',
            'post_reset_redirect': '/password/reset/done'
        }, name='password_reset_view'
    ),
    url(
        r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        password_reset_confirm, {
            'template_name': 'appearance/password_reset_confirm.html',
            'post_reset_redirect': '/password/reset/complete/'
        }, name='password_reset_confirm_view'
    ),
    url(
        r'^password/reset/complete/$',
        password_reset_complete, {
            'template_name': 'appearance/password_reset_complete.html'
        }, name='password_reset_complete_view'),
    url(
        r'^password/reset/done/$',
        password_reset_done, {
            'template_name': 'appearance/password_reset_done.html'
        }, name='password_reset_done_view'),
]
