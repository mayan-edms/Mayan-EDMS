from django.contrib import messages
from django.contrib.auth import login as auth_login
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
from django.utils.decorators import classonlymethod, method_decorator
from django.utils.translation import ungettext, ugettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters

from formtools.wizard.views import SessionWizardView
from stronghold.views import StrongholdPublicMixin

import mayan
from mayan.apps.common.settings import (
    setting_home_view, setting_project_title, setting_project_url
)
from mayan.apps.user_management.permissions import permission_user_edit
from mayan.apps.user_management.querysets import get_user_queryset
from mayan.apps.views.generics import MultipleObjectFormActionView

from ..forms import AuthenticationFormUsernamePassword, EmailAuthenticationForm, UsernameAuthenticationForm
from ..settings import (
    setting_disable_password_reset, setting_login_method,
    setting_maximum_session_length
)


class LoginWizard(StrongholdPublicMixin, SessionWizardView):
    template_name = 'authentication/login.html'

    @classonlymethod
    def as_view(cls, *args, **kwargs):
        cls.authentication_backend_class = kwargs.pop('authentication_backend_class')
        cls.authentication_backend = cls.authentication_backend_class()

        cls.login_view_class = kwargs.pop('login_view_class')

        cls.form_list = cls.authentication_backend_class.form_list
        return super().as_view(*args, **kwargs)

    # ~ def dispatch(self, request, *args, **kwargs):
        # ~ #form_list = [AuthenticationFormUsernamePassword]
        # ~ condition_dict = {}

        # ~ result = self.__class__.get_initkwargs(
            # ~ condition_dict=condition_dict, form_list=form_list
        # ~ )
        # ~ self.form_list = result['form_list']
        # ~ self.condition_dict = result['condition_dict']

        # ~ return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)

        #wizard_step = AuthenticationFormUsernamePassword#DocumentCreateWizardStep.get(name=self.steps.current)
        wizard_step = self.form_list[self.steps.current]

        context.update(
            {
                'form_css_classes': 'form-hotkey-double-click',
                'step_title': _(
                    'Step %(step)d of %(total_steps)d: %(step_label)s'
                ) % {
                    'step': self.steps.step1, 'total_steps': len(self.form_list),
                    'step_label': 'label',#wizard_step.label,
                },
                'submit_label': _('Next step'),
                #'submit_icon': icon_wizard_submit,
                'title': _('Login'),
                'wizard_step': wizard_step,
                #'wizard_steps': [AuthenticationFormUsernamePassword],#DocumentCreateWizardStep.get_all(),
            }
        )
        return context

    def get_form_initial(self, step):
        return {}#DocumentCreateWizardStep.get(name=step).get_form_initial(wizard=self) or {}

    def get_form_kwargs(self, step):
        return {}#DocumentCreateWizardStep.get(name=step).get_form_kwargs(wizard=self) or {}

    def done(self, form_list, **kwargs):
        query_dict = {}

        for step in self.__class__.form_list:
            query_dict.update(step.done(wizard=self) or {})

        self.authentication_backend.login(
            cleaned_data=self.get_all_cleaned_data(), done_data=query_dict,
            form_list=form_list, request=self.request
        )

        login_view_instance = self.__class__.login_view_class()
        login_view_instance.request = self.request

        return HttpResponseRedirect(
            redirect_to=login_view_instance.get_success_url()
        )


class AuthenticationBackendRememberMeMixin:
    def login(self, cleaned_data, done_data, form_list, request):
        remember_me = cleaned_data.get('remember_me')

        # remember_me values:
        # True - long session
        # False - short session
        # None - Form has no remember_me value and we let the session
        # expiration default.

        if remember_me is True:
            request.session.set_expiry(
                setting_maximum_session_length.value
            )
        elif remember_me is False:
            request.session.set_expiry(0)

        return super().login(
            cleaned_data=cleaned_data, done_data=done_data,
            form_list=form_list, request=request
        )


class AuthenticationBackendModelUsernamePassword(AuthenticationBackendRememberMeMixin):
    form_list = [AuthenticationFormUsernamePassword]

    def login(self, cleaned_data, done_data, form_list, request):
        auth_login(request, list(form_list)[0].get_user())


class MayanMultiFactorLoginView(StrongholdPublicMixin, LoginView):
    extra_context = {
        'appearance_type': 'plain'
    }
    #template_name = 'authentication/login.html'
    #redirect_authenticated_user = True

    @classonlymethod
    def as_view(cls, **initkwargs):
        initkwargs_copy = initkwargs.copy()
        result = super().as_view(**initkwargs)

        initkwargs_copy['authentication_backend_class'] = AuthenticationBackendModelUsernamePassword
        initkwargs_copy['login_view_class'] = cls

        cls.view_function = LoginWizard.as_view(**initkwargs_copy)

        return result

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if self.redirect_authenticated_user and self.request.user.is_authenticated:
            redirect_to = self.get_success_url()
            if redirect_to == self.request.path:
                raise ValueError(
                    "Redirection loop for authenticated user detected. Check that "
                    "your LOGIN_REDIRECT_URL doesn't point to a login page."
                )
            return HttpResponseRedirect(redirect_to)
        return self.__class__.view_function(request, *args, **kwargs)


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


class MayanPasswordResetCompleteView(
    StrongholdPublicMixin, PasswordResetCompleteView
):
    extra_context = {
        'appearance_type': 'plain'
    }
    template_name = 'authentication/password_reset_complete.html'


class MayanPasswordResetConfirmView(
    StrongholdPublicMixin, PasswordResetConfirmView
):
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
    success_message = _(
        'Password change request performed on %(count)d user'
    )
    success_message_plural = _(
        'Password change request performed on %(count)d users'
    )

    def get_extra_context(self):
        queryset = self.object_list

        result = {
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
                    'title': _(
                        'Change password for user: %s'
                    ) % queryset.first()
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
