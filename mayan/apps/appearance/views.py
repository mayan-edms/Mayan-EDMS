from django.template import RequestContext
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from mayan.apps.user_management.permissions import (
    permission_user_edit, permission_user_view
)
from mayan.apps.user_management.querysets import get_user_queryset
from mayan.apps.user_management.views.view_mixins import DynamicExternalUserViewMixin
from mayan.apps.views.generics import (
    SingleObjectCreateView, SingleObjectDeleteView, SingleObjectDetailView,
    SingleObjectEditView, SingleObjectListView
)
from mayan.apps.views.mixins import ExternalObjectViewMixin

from .forms import ThemeForm, UserThemeSettingForm, UserThemeSettingForm_view
from .icons import icon_theme_setup
from .links import link_theme_create
from .models import Theme
from .permissions import (
    permission_theme_create, permission_theme_delete, permission_theme_edit,
    permission_theme_view
)


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


class UserThemeSettingsDetailsView(
    DynamicExternalUserViewMixin, ExternalObjectViewMixin,
    SingleObjectDetailView
):
    form_class = UserThemeSettingForm_view
    external_object_permission = permission_user_view
    external_object_pk_url_kwarg = 'user_id'

    def get_external_object_queryset(self):
        return get_user_queryset(user=self.request.user)

    def get_extra_context(self, **kwargs):
        return {
            'form': UserThemeSettingForm_view(
                instance=self.external_object.theme_settings
            ),
            'object': self.external_object,
            'read_only': True,
            'title': _('Theme settings for user: %s') % self.external_object
        }

    def get_object(self):
        return self.external_object.theme_settings


class UserThemeSettingsEditView(
    DynamicExternalUserViewMixin, ExternalObjectViewMixin,
    SingleObjectEditView
):
    form_class = UserThemeSettingForm
    external_object_permission = permission_user_edit
    external_object_pk_url_kwarg = 'user_id'

    def get_external_object_queryset(self):
        return get_user_queryset(user=self.request.user)

    def get_extra_context(self):
        return {
            'title': _(
                'Edit theme settings for user: %s'
            ) % self.external_object,
            'object': self.external_object
        }

    def get_instance_extra_data(self):
        return {'_event_actor': self.request.user}

    def get_object(self):
        return self.external_object.theme_settings
