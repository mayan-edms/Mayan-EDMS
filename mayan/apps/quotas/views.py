from django.http import Http404, HttpResponseRedirect
from django.template import RequestContext
from django.urls import reverse, reverse_lazy
from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.generics import (
    FormView, SingleObjectDeleteView, SingleObjectDynamicFormCreateView,
    SingleObjectDynamicFormEditView, SingleObjectListView
)

from .classes import QuotaBackend
from .forms import QuotaBackendSelectionForm, QuotaDynamicForm
from .icons import icon_quota_setup
from .links import link_quota_create
from .models import Quota
from .permissions import (
    permission_quota_create, permission_quota_delete,
    permission_quota_edit, permission_quota_view
)


class QuotaBackendSelectionView(FormView):
    extra_context = {
        'title': _('New quota backend selection'),
    }
    form_class = QuotaBackendSelectionForm
    view_permission = permission_quota_create

    def form_valid(self, form):
        backend = form.cleaned_data['backend']
        return HttpResponseRedirect(
            reverse('quotas:quota_create', args=(backend,),)
        )


class QuotaCreateView(SingleObjectDynamicFormCreateView):
    form_class = QuotaDynamicForm
    post_action_redirect = reverse_lazy('quotas:quota_list')
    view_permission = permission_quota_create

    def get_backend(self):
        try:
            return QuotaBackend.get(name=self.kwargs['class_path'])
        except KeyError:
            raise Http404(
                '{} class not found'.format(self.kwargs['class_path'])
            )

    def get_extra_context(self):
        return {
            'title': _(
                'Create a "%s" quota'
            ) % self.get_backend().label,
        }

    def get_form_extra_kwargs(self):
        return {
            'user': self.request.user
        }

    def get_form_schema(self):
        backend = self.get_backend()
        return {
            'fields': backend.get_fields(),
            'field_order': backend.get_field_order(),
            'widgets': backend.get_widgets()
        }

    def get_instance_extra_data(self):
        return {'backend_path': self.kwargs['class_path']}

    def get_save_extra_data(self):
        return {'_user': self.request.user}


class QuotaDeleteView(SingleObjectDeleteView):
    model = Quota
    object_permission = permission_quota_delete
    pk_url_kwarg = 'quota_id'
    post_action_redirect = reverse_lazy('quotas:quota_list')

    def get_extra_context(self):
        return {
            'title': _('Delete quota: %s') % self.object,
        }


class QuotaEditView(SingleObjectDynamicFormEditView):
    form_class = QuotaDynamicForm
    model = Quota
    object_permission = permission_quota_edit
    pk_url_kwarg = 'quota_id'

    def form_valid(self, form):
        return super(QuotaEditView, self).form_valid(form)

    def get_extra_context(self):
        return {
            'title': _('Edit quota: %s') % self.object,
        }

    def get_form_extra_kwargs(self):
        return {
            'user': self.request.user
        }

    def get_form_schema(self):
        backend = self.object.get_backend_class()
        return {
            'fields': backend.get_fields(),
            'field_order': backend.get_field_order(),
            'widgets': backend.get_widgets()
        }

    def get_save_extra_data(self):
        return {'_user': self.request.user}


class QuotaListView(SingleObjectListView):
    model = Quota
    object_permission = permission_quota_view

    def get_extra_context(self):
        return {
            'hide_object': True,
            'no_results_icon': icon_quota_setup,
            'no_results_main_link': link_quota_create.resolve(
                context=RequestContext(request=self.request)
            ),
            'no_results_text': _(
                'Quotas restrict usage of system resources. '
            ),
            'no_results_title': _('No quotas available'),
            'title': _('Quotas'),
        }
