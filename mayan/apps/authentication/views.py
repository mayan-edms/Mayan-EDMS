from __future__ import absolute_import, unicode_literals

from django.contrib import messages
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeDoneView, PasswordChangeView,
    PasswordResetCompleteView, PasswordResetConfirmView, PasswordResetDoneView,
    PasswordResetView
)
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils.translation import ugettext_lazy as _

from stronghold.views import StrongholdPublicMixin

import mayan
from mayan.apps.common.settings import (
    setting_home_view, setting_project_title, setting_project_url
)

from .forms import EmailAuthenticationForm, UsernameAuthenticationForm
from .settings import setting_login_method, setting_maximum_session_length


class MayanLoginView(StrongholdPublicMixin, LoginView):
    """
    Control how the use is to be authenticated, options are 'email' and
    'username'
    """
    extra_context = {
        'appearance_type': 'plain'
    }
    template_name = 'authentication/login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        result = super(MayanLoginView, self).form_valid(form=form)
        remember_me = form.cleaned_data.get('remember_me')

        # remember_me values:
        # True - long session
        # False - short session
        # None - Form has no remember_me value and we let the session
        # expiration default.

        if remember_me is True:
            self.request.session.set_expiry(
                setting_maximum_session_length.value
            )
        elif remember_me is False:
            self.request.session.set_expiry(0)

        return result

    def get_form_class(self):
        if setting_login_method.value == 'email':
            return EmailAuthenticationForm
        else:
            return UsernameAuthenticationForm


class MayanLogoutView(LogoutView):
    """No current change or overrides, left here for future expansion"""


class MayanPasswordChangeDoneView(PasswordChangeDoneView):
    def dispatch(self, *args, **kwargs):
        messages.success(
            message=_('Your password has been successfully changed.'),
            request=self.request
        )
        return redirect(to='user_management:current_user_details')


class MayanPasswordChangeView(PasswordChangeView):
    extra_context = {'title': _('Current user password change')}
    success_url = reverse_lazy(viewname='authentication:password_change_done')
    template_name = 'appearance/generic_form.html'

    def dispatch(self, *args, **kwargs):
        if self.request.user.user_options.block_password_change:
            messages.error(
                message=_(
                    'Changing the password is not allowed for this account.'
                ), request=self.request
            )
            return HttpResponseRedirect(
                redirect_to=reverse(viewname=setting_home_view.view)
            )

        return super(MayanPasswordChangeView, self).dispatch(*args, **kwargs)


class MayanPasswordResetCompleteView(StrongholdPublicMixin, PasswordResetCompleteView):
    extra_context = {
        'appearance_type': 'plain'
    }
    template_name = 'authentication/password_reset_complete.html'


class MayanPasswordResetConfirmView(StrongholdPublicMixin, PasswordResetConfirmView):
    extra_context = {
        'appearance_type': 'plain'
    }
    success_url = reverse_lazy(
        viewname='authentication:password_reset_complete_view'
    )
    template_name = 'authentication/password_reset_confirm.html'


class MayanPasswordResetDoneView(StrongholdPublicMixin, PasswordResetDoneView):
    extra_context = {
        'appearance_type': 'plain'
    }
    template_name = 'authentication/password_reset_done.html'


class MayanPasswordResetView(StrongholdPublicMixin, PasswordResetView):
    email_template_name = 'authentication/password_reset_email.html'
    extra_context = {
        'appearance_type': 'plain'
    }
    extra_email_context = {
        'project_copyright': mayan.__copyright__,
        'project_license': mayan.__license__,
        'project_title': setting_project_title.value,
        'project_website': setting_project_url.value
    }
    subject_template_name = 'authentication/password_reset_subject.txt'
    success_url = reverse_lazy(
        viewname='authentication:password_reset_done_view'
    )
    template_name = 'authentication/password_reset_form.html'
