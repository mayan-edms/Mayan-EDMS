import logging

from django.contrib import messages
from django.http import Http404, HttpResponseRedirect
from django.template import RequestContext
from django.urls import reverse, reverse_lazy
from django.utils.translation import ugettext_lazy as _

from mayan.apps.documents.permissions import permission_document_create
from mayan.apps.views.generics import (
    ConfirmView, FormView, MultipleObjectConfirmActionView,
    SingleObjectDeleteView, SingleObjectDynamicFormCreateView,
    SingleObjectDynamicFormEditView, SingleObjectListView
)
from mayan.apps.views.mixins import ExternalObjectViewMixin

from ..classes import SourceBackend
from ..forms import SourceBackendSelectionForm, SourceBackendDynamicForm
from ..icons import icon_source_list
from ..links import link_source_backend_selection
from ..models import Source
from ..permissions import (
    permission_sources_create, permission_sources_delete,
    permission_sources_edit, permission_sources_view,
)
from ..tasks import task_source_process_document

__all__ = (
    'SourceBackendSelectionView', 'SourceTestView', 'SourceCreateView',
    'SourceDeleteView', 'SourceEditView', 'SourceListView',
)
logger = logging.getLogger(name=__name__)


class SourceBackendSelectionView(FormView):
    extra_context = {
        'title': _('New source backend selection'),
    }
    form_class = SourceBackendSelectionForm
    view_permission = permission_sources_create

    def form_valid(self, form):
        backend = form.cleaned_data['backend']
        return HttpResponseRedirect(
            redirect_to=reverse(
                viewname='sources:source_create', kwargs={
                    'backend_path': backend
                }
            )
        )


class SourceActionView(MultipleObjectConfirmActionView):
    model = Source
    object_permission = permission_document_create
    pk_url_kwarg = 'source_id'

    def get_all_kwargs(self):
        kwargs = self.kwargs.copy()
        kwargs.update(self.request.GET)
        kwargs.update(self.request.POST)
        kwargs['view'] = self
        return kwargs

    def get_extra_context(self):
        return self.object.get_backend_instance().get_action_context(
            name=self.kwargs['action_name'], **self.get_all_kwargs()
        )

    def view_action(self):
        return self.object.get_backend_instance().execute_action(
            name=self.kwargs['action_name'], request=self.request,
            **self.get_all_kwargs()
        )


class SourceCreateView(SingleObjectDynamicFormCreateView):
    form_class = SourceBackendDynamicForm
    post_action_redirect = reverse_lazy(viewname='sources:source_list')
    view_permission = permission_sources_create

    def get_backend(self):
        try:
            return SourceBackend.get(name=self.kwargs['backend_path'])
        except KeyError:
            raise Http404(
                '{} class not found'.format(self.kwargs['backend_path'])
            )

    def get_extra_context(self):
        return {
            'title': _(
                'Create a "%s" source'
            ) % self.get_backend().label,
        }

    def get_form_schema(self):
        return self.get_backend().get_setup_form_schema()

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user,
            'backend_path': self.kwargs['backend_path']
        }


class SourceDeleteView(SingleObjectDeleteView):
    model = Source
    object_permission = permission_sources_delete
    pk_url_kwarg = 'source_id'
    post_action_redirect = reverse_lazy(
        viewname='sources:source_list'
    )

    def get_extra_context(self):
        return {
            'object': self.object,
            'title': _('Delete the source: %s?') % self.object,
        }


class SourceEditView(SingleObjectDynamicFormEditView):
    form_class = SourceBackendDynamicForm
    model = Source
    object_permission = permission_sources_edit
    pk_url_kwarg = 'source_id'
    post_action_redirect = reverse_lazy(
        viewname='sources:source_list'
    )

    def get_extra_context(self):
        return {
            'title': _('Edit source: %s') % self.object,
        }

    def get_form_schema(self):
        return self.object.get_backend().get_setup_form_schema()

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user
        }


class SourceListView(SingleObjectListView):
    model = Source
    object_permission = permission_sources_view

    def get_extra_context(self):
        return {
            'hide_link': True,
            'hide_object': True,
            'no_results_icon': icon_source_list,
            'no_results_main_link': link_source_backend_selection.resolve(
                context=RequestContext(request=self.request)
            ),
            'no_results_text': _(
                'Sources provide the means to upload documents. '
                'Some sources are interactive and require user input to '
                'operate. Others are automatic and run in the background '
                'without user intervention.'
            ),
            'no_results_title': _('No sources available'),
            'title': _('Sources'),
        }


class SourceTestView(ExternalObjectViewMixin, ConfirmView):
    """
    Trigger the task_source_process_document task for a given source to
    test/debug their configuration irrespective of the schedule task setup.
    """
    external_object_permission = permission_sources_edit
    external_object_pk_url_kwarg = 'source_id'
    external_object_class = Source

    def get_extra_context(self):
        return {
            'object': self.external_object,
            'subtitle': _(
                'This will execute the source code even if the source '
                'is not enabled. Sources that delete content after '
                'downloading will not do so while being tested. Check the '
                'source\'s error log for information during testing. A '
                'successful test will clear the error log.'
            ), 'title': _(
                'Trigger check for source "%s"?'
            ) % self.external_object,
        }

    def view_action(self):
        task_source_process_document.apply_async(
            kwargs={
                'source_id': self.external_object.pk, 'dry_run': True
            }
        )

        messages.success(
            message=_('Source test queued.'), request=self.request
        )
