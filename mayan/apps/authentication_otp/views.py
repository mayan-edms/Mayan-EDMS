from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from mayan.apps.views.generics import (
    ConfirmView, FormView, SingleObjectDetailView
)

from .forms import FormUserOTPDataDetail, FormUserOTPDataEdit


class UserOTPDataDetailView(SingleObjectDetailView):
    form_class = FormUserOTPDataDetail

    def get_extra_context(self):
        return {
            'object': self.object,
            'title': _(
                'One time pad details for user: %s'
            ) % self.object
        }

    def get_object(self):
        return self.request.user


class UserOTPDataDisableView(ConfirmView):
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request=request, *args, **kwargs)

    def get_extra_context(self):
        return {
            'object': self.object,
            'title': _(
                'Disable one time pad for user: %s'
            ) % self.object
        }

    def get_object(self):
        return self.request.user

    def view_action(self):
        self.request.user.otp_data.disable()

        messages.success(
            request=self.request, message=_('OTP disable successfully.')
        )


class UserOTPDataEnableView(FormView):
    form_class = FormUserOTPDataEdit

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()

        if request.user.otp_data.is_enabled():
            messages.info(
                request=self.request, message=_('OTP is already enabled.')
            )
            return HttpResponseRedirect(
                redirect_to=reverse(
                    viewname='authentication_otp:otp_detail'
                )
            )
        else:
            return super().dispatch(request=request, *args, **kwargs)

    def form_valid(self, form):
        secret = form.cleaned_data['secret']
        token = form.cleaned_data['token']
        self.request.user.otp_data.enable(secret=secret, token=token)

        messages.success(
            request=self.request, message=_('OTP enabled successfully.')
        )

        return super().form_valid(form=form)

    def get_extra_context(self):
        return {
            'object': self.object,
            'title': _(
                'Enable one time pad for user: %s'
            ) % self.object
        }

    def get_object(self):
        return self.request.user
