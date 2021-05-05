from django.template import RequestContext
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from mayan.apps.views.generics import (
    SingleObjectCreateView, SingleObjectDeleteView, SingleObjectEditView,
    SingleObjectListView, SimpleView
)

from .forms import ThemeForm, UserThemeSettingForm, UserThemeSettingForm_view
from .icons import icon_theme_setup
from .links import link_theme_create
from .models import Theme
from .permissions import (
    permission_theme_create, permission_theme_delete, permission_theme_edit,
    permission_theme_view
)


class CurrentUserThemeSettingsDetailsView(SimpleView):
    template_name = 'appearance/generic_form.html'

    def get_extra_context(self, **kwargs):
        return {
            'form': UserThemeSettingForm_view(
                instance=self.request.user.theme_settings
            ),
            'read_only': True,
            'title': _('Current user theme settings details'),
        }


class CurrentUserThemeSettingsEditView(SingleObjectEditView):
    extra_context = {
        'title': _('Edit current user theme settings details')
    }
    form_class = UserThemeSettingForm
    post_action_redirect = reverse_lazy(
        viewname='appearance:current_user_theme_settings_details'
    )

    def get_object(self):
        return self.request.user.theme_settings


class ThemeCreateView(SingleObjectCreateView):
    extra_context = {'title': _('Create new theme')}
    form_class = ThemeForm
    post_action_redirect = reverse_lazy(
        viewname='appearance:theme_list'
    )
    view_permission = permission_theme_create

    def get_instance_extra_data(self):
        return {'_event_actor': self.request.user}


class ThemeDeleteView(SingleObjectDeleteView):
    model = Theme
    object_permission = permission_theme_delete
    pk_url_kwarg = 'theme_id'
    post_action_redirect = reverse_lazy(
        viewname='appearance:theme_list'
    )

    def get_extra_context(self):
        return {
            'object': self.object,
            'title': _('Delete theme: %s') % self.object
        }


class ThemeEditView(SingleObjectEditView):
    form_class = ThemeForm
    model = Theme
    object_permission = permission_theme_edit
    pk_url_kwarg = 'theme_id'
    post_action_redirect = reverse_lazy(
        viewname='appearance:theme_list'
    )

    def get_extra_context(self):
        return {
            'object': self.object,
            'title': _('Edit theme: %s') % self.object
        }

    def get_instance_extra_data(self):
        return {'_event_actor': self.request.user}


class ThemeListView(SingleObjectListView):
    model = Theme
    object_permission = permission_theme_view

    def get_extra_context(self):
        return {
            'hide_link': True,
            'hide_object': True,
            'no_results_icon': icon_theme_setup,
            'no_results_main_link': link_theme_create.resolve(
                context=RequestContext(request=self.request)
            ),
            'no_results_text': _(
                'Themes allow changing the visual appearance without '
                'requiring code changes.'
            ),
            'no_results_title': _(
                'There are no themes'
            ),
            'title': _('Themes'),
        }
