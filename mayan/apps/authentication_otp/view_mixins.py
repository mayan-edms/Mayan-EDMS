from django.http import HttpResponseRedirect
from django.urls import reverse

from mayan.apps.common.settings import setting_home_view

from .utils import is_otp_backend_enabled


class OTPBackendEnabledViewMixin:
    def dispatch(self, request, *args, **kwargs):
        if not is_otp_backend_enabled():
            return HttpResponseRedirect(
                redirect_to=reverse(viewname=setting_home_view.value)
            )
        else:
            return super().dispatch(request=request, *args, **kwargs)
