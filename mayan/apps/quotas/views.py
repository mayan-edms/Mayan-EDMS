from __future__ import absolute_import, unicode_literals

from django.http import Http404, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils.translation import ugettext_lazy as _

from common.generics import (
    FormView, SingleObjectDeleteView, SingleObjectDynamicFormCreateView,
    SingleObjectDynamicFormEditView, SingleObjectListView
)

from .classes import QuotaBackend
from .forms import QuotaBackendSelectionForm, QuotaDynamicForm
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

    def get_form_schema(self):
        return {
            'fields': self.get_backend().fields,
            'widgets': getattr(self.get_backend(), 'widgets', {})
        }

    def get_instance_extra_data(self):
        return {'backend_path': self.kwargs['class_path']}


class QuotaDeleteView(SingleObjectDeleteView):
    object_permission = permission_quota_delete
    post_action_redirect = reverse_lazy('quotas:quota_list')

    def get_extra_context(self):
        return {
            'title': _('Delete quota: %s') % self.get_object(),
        }

    def get_queryset(self):
        return Quota.objects.filter(editable=True)


class QuotaEditView(SingleObjectDynamicFormEditView):
    form_class = QuotaDynamicForm
    object_permission = permission_quota_edit

    def form_valid(self, form):
        return super(QuotaEditView, self).form_valid(form)

    def get_extra_context(self):
        return {
            'title': _('Edit quota: %s') % self.get_object(),
        }

    def get_form_schema(self):
        return {
            'fields': self.get_object().get_backend_class().fields,
            'widgets': getattr(
                self.get_object().get_backend_class(), 'widgets', {}
            )
        }

    def get_queryset(self):
        return Quota.objects.filter(editable=True)


class QuotaListView(SingleObjectListView):
    extra_context = {
        'hide_object': True,
        'title': _('Quotas'),
    }
    model = Quota
    object_permission = permission_quota_view
