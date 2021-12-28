from collections import OrderedDict

from django.contrib import messages
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeDoneView, PasswordChangeView,
    PasswordResetCompleteView, PasswordResetConfirmView,
    PasswordResetDoneView, PasswordResetView
)
from django.core.exceptions import PermissionDenied
from django.forms import formsets
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import classonlymethod
from django.utils.translation import ungettext, ugettext_lazy as _

from formtools.wizard.views import SessionWizardView
from stronghold.views import StrongholdPublicMixin

import mayan
from mayan.apps.common.settings import (
    setting_home_view, setting_project_title, setting_project_url
)
from mayan.apps.user_management.permissions import permission_user_edit
from mayan.apps.user_management.querysets import get_user_queryset
from mayan.apps.views.generics import MultipleObjectFormActionView

from ..classes import AuthenticationBackend
from ..forms import AuthenticationFormBase
from ..settings import setting_disable_password_reset


class MayanMultiStepLoginView(
    StrongholdPublicMixin, SessionWizardView, LoginView
):
    extra_context = {
        'appearance_type': 'plain'
    }
    redirect_authenticated_user = True
    template_name = 'authentication/login.html'

    @staticmethod
    def form_list_property(self):
        """
        Return the processed form list after the view has initialized.
        """
        self.authentication_backend = AuthenticationBackend.get_instance()

        form_list = self.authentication_backend.get_form_list()

        computed_form_list = OrderedDict()

        for form_index, form in enumerate(iterable=form_list):
            computed_form_list[str(form_index)] = form

        for form in computed_form_list.values():
            if issubclass(form, formsets.BaseFormSet):
                form = form.form

        return computed_form_list

    @classonlymethod
    def as_view(cls, *args, **kwargs):
        # SessionWizardView needs at least one form in order to be
        # initialized as a view. Declare one empty form and then change the
        # form list in the .dispatch() method.
        class EmptyForm(AuthenticationFormBase):
            """Empty form"""

        cls.form_list = [EmptyForm]

        # Allow super to initialize and pass the form_list len() assert
        # before replacing the form_list attribute with our property.
        result = super().as_view(*args, **kwargs)

        def null_setter(self, value):
            return

        cls.form_list = property(
            fget=MayanMultiStepLoginView.form_list_property,
            fset=null_setter
        )

        return result

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)

        wizard_step = self.form_list[self.steps.current]

        if self.storage.current_step == self.steps.last:
            context['submit_label'] = None
        else:
            context['submit_label'] = _('Next')

        context.update(
            {
                'form_css_classes': 'form-hotkey-double-click',
                'step_title': _(
                    'Step %(step)d of %(total_steps)d: %(step_label)s'
                ) % {
                    'step': self.steps.step1, 'total_steps': len(self.form_list),
                    'step_label': wizard_step._label
                },
                'wizard_step': wizard_step,
                'wizard_steps': self.form_list
            }
        )
        return context

    def get_form_kwargs(self, step):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        kwargs['wizard'] = self
        return kwargs

    def done(self, form_list, **kwargs):
        self.authentication_backend.login(
            form_list=form_list, request=self.request,
            kwargs=self.get_all_cleaned_data()
        )

        return HttpResponseRedirect(
            redirect_to=self.get_success_url()
        )


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
