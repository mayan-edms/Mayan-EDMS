from django.conf import settings
from django.contrib import messages
from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils import timezone, translation
from django.utils.translation import ugettext_lazy as _
from django.views.generic import RedirectView

from mayan.apps.views.generics import (
    ConfirmView, SingleObjectEditView, SimpleView
)
from mayan.apps.views.mixins import (
    ExternalContentTypeObjectMixin, ObjectNameMixin
)

from .classes import ModelCopy
from .forms import (
    LicenseForm, LocaleProfileForm, LocaleProfileForm_view,
)
from .icons import icon_setup
from .menus import menu_tools, menu_setup
from .permissions import permission_object_copy
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


class ObjectCopyView(ExternalContentTypeObjectMixin, ObjectNameMixin, ConfirmView):
    external_object_permission = permission_object_copy

    def get_extra_context(self):
        model_copy = ModelCopy.get(model=self.external_object._meta.model)
        context = {
            'object': self.external_object,
            'subtitle': _('Fields to be copied: %s') % ', '.join(
                sorted(
                    map(
                        str, model_copy.get_fields_verbose_names()
                    )
                )
            )
        }

        context['title'] = _('Make a copy of %(object_name)s "%(object)s"?') % {
            'object_name': self.get_object_name(context=context), 'object': self.external_object
        }

        return context

    def view_action(self):
        self.external_object.copy_instance()
        messages.success(
            message=_('Object copied successfully.'),
            request=self.request
        )


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
