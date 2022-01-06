from django.conf.urls import url
from django.urls import path

from .views.authentication_views import (
    MayanLoginView, MayanLogoutView, MayanPasswordChangeDoneView,
    MayanPasswordChangeView, MayanPasswordResetCompleteView,
    MayanPasswordResetConfirmView, MayanPasswordResetDoneView,
    MayanPasswordResetView, MultiFactorAuthenticationView,
    UserSetPasswordView
)
from .views.impersonation_views import (
    UserImpersonateEndView, UserImpersonateFormStartView,
    UserImpersonateStartView
)


urlpatterns_authenticattion = [
    url(
        regex=r'^login/$', name='login_view',
        view=MayanLoginView.as_view()
    ),
    url(
        regex=r'^login/multi_factor_authentication/$',
        name='multi_factor_authentication_view',
        view=MultiFactorAuthenticationView.as_view()
    ),
    url(
        regex=r'^logout/$', view=MayanLogoutView.as_view(), name='logout_view'
    ),
]

urlpatterns_password = [
    url(
        regex=r'^password/change/done/$', name='password_change_done',
        view=MayanPasswordChangeDoneView.as_view()
    ),
    url(
        regex=r'^password/change/$', name='password_change_view',
        view=MayanPasswordChangeView.as_view()
    ),
    url(
        regex=r'^password/reset/complete/$',
        name='password_reset_complete_view',
        view=MayanPasswordResetCompleteView.as_view()
    ),
    path(
        'password/reset/confirm/<uidb64>/<token>/',
        name='password_reset_confirm_view',
        view=MayanPasswordResetConfirmView.as_view()
    ),
    url(
        regex=r'^password/reset/done/$',
        name='password_reset_done_view',
        view=MayanPasswordResetDoneView.as_view()
    ),
    url(
        regex=r'^password/reset/$', name='password_reset_view',
        view=MayanPasswordResetView.as_view()
    ),
    url(
        regex=r'^users/(?P<user_id>\d+)/set_password/$',
        name='user_set_password', view=UserSetPasswordView.as_view()
    ),
    url(
        regex=r'^users/multiple/set_password/$',
        name='user_multiple_set_password', view=UserSetPasswordView.as_view()
    )
]

urlpatterns_user_impersonation = [
    url(
        regex=r'^impersonate/end/$', name='user_impersonate_end',
        view=UserImpersonateEndView.as_view()
    ),
    url(
        regex=r'^impersonate/start/$', name='user_impersonate_form_start',
        view=UserImpersonateFormStartView.as_view()
    ),
    url(
        regex=r'^impersonate/(?P<user_id>\d+)/start/$',
        name='user_impersonate_start', view=UserImpersonateStartView.as_view()
    )
]

urlpatterns = []
urlpatterns.extend(urlpatterns_authenticattion)
urlpatterns.extend(urlpatterns_password)
urlpatterns.extend(urlpatterns_user_impersonation)
