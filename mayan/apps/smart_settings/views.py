from django.conf import settings
from django.contrib import messages
from django.http import Http404
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from mayan.apps.views.generics import FormView, SingleObjectListView

from .classes import SettingNamespace, Setting
from .forms import SettingForm
from .icons import (
    icon_setting_namespace_detail, icon_setting_namespace_list,
    icon_setting_edit
)
from .permissions import permission_settings_edit, permission_settings_view


class SettingEditView(FormView):
    form_class = SettingForm
    view_icon = icon_setting_edit
    view_permission = permission_settings_edit

    def dispatch(self, request, *args, **kwargs):
        if settings.COMMON_DISABLE_LOCAL_STORAGE:
            messages.warning(
                message=_(
                    'Local storage is currently disabled, changes to '
                    'setting values will not be saved or take effect.'
                ), request=self.request
            )

        return super().dispatch(request=request, *args, **kwargs)

    def form_valid(self, form):
        self.get_object().value = form.cleaned_data['value']
        Setting.save_configuration()
        messages.success(
            message=_('Setting updated successfully.'),
            request=self.request
        )
        return super().form_valid(form=form)

    def get_extra_context(self):
        return {
            'hide_link': True,
            'object': self.get_object(),
            'title': _('Edit setting: %s') % self.get_object(),
        }

    def get_initial(self):
        return {'setting': self.get_object()}

    def get_object(self):
        return Setting.get(self.kwargs['setting_global_name'])

    def get_post_action_redirect(self):
        return reverse(
            viewname='settings:setting_namespace_detail', kwargs={
                'namespace_name': self.get_object().namespace.name
            }
        )


class SettingNamespaceDetailView(SingleObjectListView):
    view_icon = icon_setting_namespace_detail
    view_permission = permission_settings_view

    def get_extra_context(self):
        return {
            'hide_object': True,
            'object': self.get_namespace(),
            'subtitle': _(
                'Settings inherited from an environment variable take '
                'precedence and cannot be changed in this view. '
            ),
            'title': _('Settings in namespace: %s') % self.get_namespace(),
        }

    def get_namespace(self):
        try:
            return SettingNamespace.get(name=self.kwargs['namespace_name'])
        except KeyError:
            raise Http404(
                _('Namespace: %s, not found') % self.kwargs['namespace_name']
            )

    def get_source_queryset(self):
        return self.get_namespace().settings


class SettingNamespaceListView(SingleObjectListView):
    extra_context = {
        'hide_link': True,
        'title': _('Setting namespaces'),
    }
    view_icon = icon_setting_namespace_list
    view_permission = permission_settings_view

    def get_source_queryset(self):
        return SettingNamespace.get_all()
