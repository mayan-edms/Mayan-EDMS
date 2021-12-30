from django.conf.urls import url

from .views import (
    UserOTPDataDetailView, UserOTPDataDisableView, UserOTPDataEnableView
)


urlpatterns = [
    url(
        regex=r'^otp/$', name='otp_detail',
        view=UserOTPDataDetailView.as_view()
    ),
    url(
        regex=r'^otp/disable/$', name='otp_disable',
        view=UserOTPDataDisableView.as_view()
    ),
    url(
        regex=r'^otp/enable/$', name='otp_enable',
        view=UserOTPDataEnableView.as_view()
    )
]
