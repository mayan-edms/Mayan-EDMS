from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone, translation
from django.utils.translation import ugettext_lazy as _
from django.views.generic import RedirectView

from mayan.apps.acls.models import AccessControlList

from .forms import (
    LicenseForm, LocaleProfileForm, LocaleProfileForm_view,
)
from .generics import (
    ConfirmView, SingleObjectEditView, SingleObjectListView, SimpleView
)
from .icons import icon_object_errors, icon_setup
from .menus import menu_tools, menu_setup
from .permissions_runtime import permission_error_log_view
from .settings import setting_home_view


class AboutView(SimpleView):
    extra_context = {'title': _('About')}
    template_name = 'appearance/about.html'


class CurrentUserLocaleProfileDetailsView(SimpleView):
    template_name = 'appearance/generic_form.html'

    def get_extra_context(self, **kwargs):
        return {
            'form': LocaleProfileForm_view(
                instance=self.request.user.locale_profile
            ),
            'read_only': True,
            'title': _('Current user locale profile details'),
        }


class CurrentUserLocaleProfileEditView(SingleObjectEditView):
    extra_context = {
        'title': _('Edit current user locale profile details')
    }
    form_class = LocaleProfileForm
    post_action_redirect = reverse_lazy(
        viewname='common:current_user_locale_profile_details'
    )

    def form_valid(self, form):
        form.save()

        timezone.activate(timezone=form.cleaned_data['timezone'])
        translation.activate(language=form.cleaned_data['language'])

        if hasattr(self.request, 'session'):
            self.request.session[
                translation.LANGUAGE_SESSION_KEY
            ] = form.cleaned_data['language']
            self.request.session[
                settings.TIMEZONE_SESSION_KEY
            ] = form.cleaned_data['timezone']
        else:
            self.request.set_cookie(
                settings.LANGUAGE_COOKIE_NAME, form.cleaned_data['language']
            )
            self.request.set_cookie(
                settings.TIMEZONE_COOKIE_NAME, form.cleaned_data['timezone']
            )

        return super(CurrentUserLocaleProfileEditView, self).form_valid(
            form=form
        )

    def get_object(self):
        return self.request.user.locale_profile


class FaviconRedirectView(RedirectView):
    permanent = True

    def get_redirect_url(self, *args, **kwargs):
        """
        Hide the static tag import to avoid errors with static file
        processors
        """
        from django.contrib.staticfiles.templatetags.staticfiles import static
        return static(path='appearance/images/favicon.ico')


class HomeView(SimpleView):
    extra_context = {
        'title': _('Dashboard'),
    }
    template_name = 'appearance/home.html'


class LicenseView(SimpleView):
    extra_context = {
        'form': LicenseForm(),
        'read_only': True,
        'title': _('License'),
    }
    template_name = 'appearance/generic_form.html'


class ObjectErrorLogEntryListClearView(ConfirmView):
    def get_extra_context(self):
        return {
            'object': self.get_object(),
            'title': _('Clear error log entries for: %s' % self.get_object()),
        }

    def get_object(self):
        content_type = get_object_or_404(
            klass=ContentType, app_label=self.kwargs['app_label'],
            model=self.kwargs['model']
        )

        return get_object_or_404(
            klass=content_type.model_class(),
            pk=self.kwargs['object_id']
        )

    def view_action(self):
        self.get_object().error_logs.all().delete()
        messages.success(
            message=_('Object error log cleared successfully'),
            request=self.request
        )


class ObjectErrorLogEntryListView(SingleObjectListView):
    def dispatch(self, request, *args, **kwargs):
        AccessControlList.objects.check_access(
            obj=self.get_object(), permissions=(permission_error_log_view,),
            user=request.user
        )

        return super(ObjectErrorLogEntryListView, self).dispatch(
            request, *args, **kwargs
        )

    def get_extra_context(self):
        return {
            'extra_columns': (
                {'name': _('Date and time'), 'attribute': 'datetime'},
                {'name': _('Result'), 'attribute': 'result'},
            ),
            'hide_object': True,
            'no_results_icon': icon_object_errors,
            'no_results_text': _(
                'This view displays the error log of different object. '
                'An empty list is a good thing.'
            ),
            'no_results_title': _(
                'There are no error log entries'
            ),
            'object': self.get_object(),
            'title': _('Error log entries for: %s' % self.get_object()),
        }

    def get_object(self):
        content_type = get_object_or_404(
            klass=ContentType, app_label=self.kwargs['app_label'],
            model=self.kwargs['model']
        )

        return get_object_or_404(
            klass=content_type.model_class(), pk=self.kwargs['object_id']
        )

    def get_source_queryset(self):
        return self.get_object().error_logs.all()


class RootView(SimpleView):
    extra_context = {'home_view': setting_home_view.value}
    template_name = 'appearance/root.html'


class SetupListView(SimpleView):
    template_name = 'appearance/generic_list_horizontal.html'

    def get_extra_context(self, **kwargs):
        return {
            'no_results_icon': icon_setup,
            'no_results_label': _('No setup options available.'),
            'no_results_text': _(
                'No results here means that don\'t have the required '
                'permissions to perform administrative task.'
            ),
            'resolved_links': menu_setup.resolve(
                request=self.request, sort_results=True
            ),
            'title': _('Setup items'),
            'subtitle': _(
                'Here you can configure all aspects of the system.'
            )
        }


class ToolsListView(SimpleView):
    template_name = 'appearance/generic_list_horizontal.html'

    def get_extra_context(self):
        return {
            'resolved_links': menu_tools.resolve(
                request=self.request, sort_results=True
            ),
            'title': _('Tools'),
            'subtitle': _(
                'These modules are used to do system maintenance.'
            )
        }
