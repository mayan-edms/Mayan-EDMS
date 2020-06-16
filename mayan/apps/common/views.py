from django.conf import settings
from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils import timezone, translation
from django.utils.translation import ugettext_lazy as _
from django.views.generic import RedirectView

from mayan.apps.views.generics import SingleObjectEditView, SimpleView

from .forms import (
    LicenseForm, LocaleProfileForm, LocaleProfileForm_view,
)
from .icons import icon_setup
from .menus import menu_tools, menu_setup
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
