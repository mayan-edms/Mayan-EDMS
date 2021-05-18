from django.contrib import messages
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeDoneView, PasswordChangeView,
    PasswordResetCompleteView, PasswordResetConfirmView,
    PasswordResetDoneView, PasswordResetView
)
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils.translation import ungettext, ugettext_lazy as _
from django.views.generic.base import View

from stronghold.views import StrongholdPublicMixin

import mayan
from mayan.apps.common.settings import (
    setting_home_view, setting_project_title, setting_project_url
)
from mayan.apps.user_management.permissions import permission_user_edit
from mayan.apps.user_management.querysets import get_user_queryset
from mayan.apps.views.http import URL
from mayan.apps.views.generics import FormView, MultipleObjectFormActionView
from mayan.apps.views.mixins import ExternalObjectViewMixin, RedirectionViewMixin

from .forms import (
    EmailAuthenticationForm, UsernameAuthenticationForm,
    UserImpersonationOptionsForm, UserImpersonationSelectionForm,
)
from .literals import (
    USER_IMPERSONATE_VARIABLE_ID, USER_IMPERSONATE_VARIABLE_DISABLE,
    USER_IMPERSONATE_VARIABLE_PERMANENT
)
from .permissions import permission_users_impersonate
from .settings import (
    setting_disable_password_reset, setting_login_method,
    setting_maximum_session_length
)


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
        result = super().form_valid(form=form)
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

        return super().dispatch(*args, **kwargs)


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

    def get(self, *args, **kwargs):
        if setting_disable_password_reset.value:
            return redirect(to=setting_home_view.value)
        return super().get(*args, **kwargs)

    def post(self, *args, **kwargs):
        if setting_disable_password_reset.value:
            return redirect(to=setting_home_view.value)
        return super().post(*args, **kwargs)


class UserSetPasswordView(MultipleObjectFormActionView):
    form_class = SetPasswordForm
    object_permission = permission_user_edit
    pk_url_kwarg = 'user_id'
    source_queryset = get_user_queryset()
    success_message = _('Password change request performed on %(count)d user')
    success_message_plural = _(
        'Password change request performed on %(count)d users'
    )

    def get_extra_context(self):
        queryset = self.object_list

        result = {
            'submit_label': _('Submit'),
            'title': ungettext(
                singular='Change user password',
                plural='Change users passwords',
                number=queryset.count()
            )
        }

        if queryset.count() == 1:
            result.update(
                {
                    'object': queryset.first(),
                    'title': _('Change password for user: %s') % queryset.first()
                }
            )

        return result

    def get_form_extra_kwargs(self):
        queryset = self.object_list
        result = {}
        if queryset:
            result['user'] = queryset.first()
            return result
        else:
            raise PermissionDenied

    def object_action(self, form, instance):
        try:
            instance.set_password(form.cleaned_data['new_password1'])
            instance.save()
            messages.success(
                message=_(
                    'Successful password reset for user: %s.'
                ) % instance, request=self.request
            )
        except Exception as exception:
            messages.error(
                message=_(
                    'Error reseting password for user "%(user)s": %(error)s'
                ) % {
                    'user': instance, 'error': exception
                }, request=self.request
            )


class UserImpersonateEndView(RedirectionViewMixin, View):
    def get(self, request, *args, **kwargs):
        url = URL(
            viewname=setting_home_view.value, query={
                USER_IMPERSONATE_VARIABLE_DISABLE: ''
            }
        )
        return HttpResponseRedirect(redirect_to=url.to_string())


class UserImpersonateFormStartView(FormView):
    form_class = UserImpersonationSelectionForm

    def form_valid(self, form):
        query = {
            USER_IMPERSONATE_VARIABLE_ID: form.cleaned_data['user_to_impersonate'].pk
        }
        if form.cleaned_data['permanent']:
            query[USER_IMPERSONATE_VARIABLE_PERMANENT] = ''

        url = URL(
            viewname=setting_home_view.value, query=query
        )
        return HttpResponseRedirect(redirect_to=url.to_string())

    def get_extra_context(self):
        return {
            'title': _('Impersonate user')
        }

    def get_form_extra_kwargs(self):
        return {
            'user': self.request.user
        }


class UserImpersonateStartView(ExternalObjectViewMixin, FormView):
    external_object_queryset = get_user_queryset()
    external_object_permission = permission_users_impersonate
    external_object_pk_url_kwarg = 'user_id'
    form_class = UserImpersonationOptionsForm

    def form_valid(self, form):
        query = {USER_IMPERSONATE_VARIABLE_ID: self.external_object.pk}
        if form.cleaned_data['permanent']:
            query[USER_IMPERSONATE_VARIABLE_PERMANENT] = ''

        url = URL(
            query=query, viewname=setting_home_view.value
        )
        return HttpResponseRedirect(redirect_to=url.to_string())

    def get_extra_context(self):
        return {
            'object': self.external_object,
            'title': _('Impersonate user: %s') % self.external_object
        }
