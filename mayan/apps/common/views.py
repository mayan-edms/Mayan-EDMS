from django.contrib import messages
from django.templatetags.static import static
from django.utils.translation import ugettext_lazy as _
from django.views.generic import RedirectView

from stronghold.views import StrongholdPublicMixin

from mayan.apps.views.generics import ConfirmView, SimpleView
from mayan.apps.views.mixins import (
    ExternalContentTypeObjectViewMixin, ObjectNameViewMixin
)

from .classes import ModelCopy
from .forms import LicenseForm
from .icons import (
    icon_about, icon_home, icon_license, icon_object_copy, icon_setup,
    icon_tools
)
from .menus import menu_tools, menu_setup
from .permissions import permission_object_copy
from .settings import setting_home_view


class AboutView(SimpleView):
    extra_context = {'title': _('About')}
    template_name = 'appearance/about.html'
    view_icon = icon_about


class FaviconRedirectView(RedirectView):
    permanent = True

    def get_redirect_url(self, *args, **kwargs):
        """
        Hide the static tag import to avoid errors with static file
        processors.
        """
        return static(path='appearance/images/favicon.ico')


class HomeView(SimpleView):
    extra_context = {
        'title': _('Home'),
    }
    template_name = 'appearance/home.html'
    view_icon = icon_home


class LicenseView(SimpleView):
    extra_context = {
        'form': LicenseForm(),
        'read_only': True,
        'title': _('License'),
    }
    template_name = 'appearance/generic_form.html'
    view_icon = icon_license


class ObjectCopyView(
    ExternalContentTypeObjectViewMixin, ObjectNameViewMixin, ConfirmView
):
    external_object_permission = permission_object_copy
    view_icon = icon_object_copy

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

        context['title'] = _(
            'Make a copy of %(object_name)s "%(object)s"?'
        ) % {
            'object_name': self.get_object_name(context=context),
            'object': self.external_object
        }

        return context

    def view_action(self):
        self.external_object.copy_instance()
        messages.success(
            message=_('Object copied successfully.'),
            request=self.request
        )


class RootView(StrongholdPublicMixin, SimpleView):
    extra_context = {'home_view': setting_home_view.value}
    template_name = 'appearance/root.html'


class SetupListView(SimpleView):
    template_name = 'appearance/generic_list_horizontal.html'
    view_icon = icon_setup

    def get_extra_context(self, **kwargs):
        return {
            'no_results_icon': icon_setup,
            'no_results_text': _(
                'No results here means that don\'t have the required '
                'permissions to perform administrative task.'
            ),
            'no_results_title': _('No setup options available.'),
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
    view_icon = icon_tools

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
