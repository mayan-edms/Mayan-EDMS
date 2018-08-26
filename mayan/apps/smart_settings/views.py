from __future__ import unicode_literals

from django.contrib import messages
from django.http import Http404
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from common.views import FormView, SingleObjectListView

from .classes import Namespace, Setting
from .forms import SettingForm
from .permissions import permission_settings_edit, permission_settings_view


class NamespaceListView(SingleObjectListView):
    extra_context = {
        'hide_link': True,
        'title': _('Setting namespaces'),
    }
    view_permission = permission_settings_view

    def get_object_list(self):
        return Namespace.get_all()


class NamespaceDetailView(SingleObjectListView):
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
            return Namespace.get(self.kwargs['namespace_name'])
        except KeyError:
            raise Http404(
                _('Namespace: %s, not found') % self.kwargs['namespace_name']
            )

    def get_object_list(self):
        return self.get_namespace().settings


class SettingEditView(FormView):
    form_class = SettingForm
    view_permission = permission_settings_edit

    def form_valid(self, form):
        self.get_object().value = form.cleaned_data['value']
        Setting.save_configuration()
        messages.success(
            self.request, _('Setting updated successfully.')
        )
        return super(SettingEditView, self).form_valid(form=form)

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
            'settings:namespace_detail', args=(
                self.get_object().namespace.name,
            )
        )
