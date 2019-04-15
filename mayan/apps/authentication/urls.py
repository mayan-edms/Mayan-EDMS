from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import url
from django.contrib.auth.views import logout

from .views import (
    login_view, password_change_done, password_change_view,
    password_reset_complete_view, password_reset_confirm_view,
    password_reset_done_view, password_reset_view
)


urlpatterns = [
    url(regex=r'^login/$', view=login_view, name='login_view'),
    url(
        regex=r'^password/change/done/$', view=password_change_done,
        name='password_change_done'
    ),
    url(
        regex=r'^password/change/$', view=password_change_view,
        name='password_change_view'
    ),
    url(
        regex=r'^logout/$', view=logout, kwargs={'next_page': settings.LOGIN_REDIRECT_URL},
        name='logout_view'
    ),
    url(
        regex=r'^password/reset/$', view=password_reset_view, name='password_reset_view'
    ),
    url(
        regex=r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        view=password_reset_confirm_view, name='password_reset_confirm_view'
    ),
    url(
        regex=r'^password/reset/complete/$', view=password_reset_complete_view,
        name='password_reset_complete_view'
    ),
    url(
        regex=r'^password/reset/done/$', view=password_reset_done_view,
        name='password_reset_done_view'
    ),
]
