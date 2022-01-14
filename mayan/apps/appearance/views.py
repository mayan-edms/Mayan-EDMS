from django.contrib.auth import get_user_model
from django.template import RequestContext
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from mayan.apps.user_management.permissions import (
    permission_user_edit, permission_user_view
)
from mayan.apps.user_management.querysets import get_user_queryset
from mayan.apps.views.generics import (
    SingleObjectCreateView, SingleObjectDeleteView, SingleObjectDetailView,
    SingleObjectEditView, SingleObjectListView, SimpleView
)


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




# ~ from .forms import LocaleProfileForm, LocaleProfileForm_view
        # ~ regex=r'^user/(?P<user_id>\d+)/locale/edit/$',


# ~ class UserLocaleProfileDetailView(SingleObjectDetailView):
    # ~ form_class = LocaleProfileForm_view
    # ~ #model = get_user_model()
    # ~ pk_url_kwarg = 'user_id'

    # ~ def get_extra_context(self, **kwargs):
        # ~ return {
            # ~ 'form': LocaleProfileForm_view(
                # ~ instance=self.object.locale_profile
            # ~ ),
            # ~ 'object': self.object,
            # ~ 'read_only': True,
            # ~ 'title': _('Locale profile for user: %s') % self.object
        # ~ }

    # ~ def get_object_permission(self):
        # ~ if self.get_object == self.request.user:
            # ~ return
        # ~ else:
            # ~ return permission_user_view

    # ~ def get_source_queryset(self):
        # ~ if self.request.user.is_superuser or self.request.user.is_staff:
            # ~ return get_user_model().objects.all()
        # ~ else:
            # ~ return get_user_queryset()


class UserThemeSettingsDetailsView(SingleObjectDetailView):
    # ~ template_name = 'appearance/generic_form.html'
    form_class = UserThemeSettingForm_view
    #model = get_user_model()
    pk_url_kwarg = 'user_id'

    def get_extra_context(self, **kwargs):
        return {
            'form': UserThemeSettingForm_view(
                instance=self.object.theme_settings
            ),
            'object': self.object,
            'read_only': True,
            'title': _('Theme settings for user: %s') % self.object
        }

    def get_object_permission(self):
        if self.get_object == self.request.user:
            return
        else:
            return permission_user_view

    def get_source_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return get_user_model().objects.all()
        else:
            return get_user_queryset()


class UserThemeSettingsEditView(SingleObjectEditView):
    # ~ extra_context = {
        # ~ 'title': _('Edit current user theme settings details')
    # ~ }
    form_class = UserThemeSettingForm
    # ~ post_action_redirect = reverse_lazy(
        # ~ viewname='appearance:user_theme_settings_details'
    # ~ )
    pk_url_kwarg = 'user_id'

    def get_extra_context(self, **kwargs):
        return {
            'object': self.object,
            'title': _('Edit theme settings for user: %s') % self.object
        }

    def get_object_permission(self):
        if self.get_object == self.request.user:
            return
        else:
            return permission_user_edit

    def get_source_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return get_user_model().objects.all()
        else:
            return get_user_queryset()

