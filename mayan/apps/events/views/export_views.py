from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

from actstream.models import Action

from mayan.apps.common.classes import QuerysetParametersSerializer
from mayan.apps.views.generics import ConfirmView
from mayan.apps.views.mixins import ExternalContentTypeObjectViewMixin

from ..classes import EventType
from ..permissions import permission_events_export
from ..tasks import task_event_queryset_export

__all__ = (
    'CurrentUserEventExportView', 'EventListExportView',
    'ObjectEventExportView', 'VerbEventExportView'
)


class EventExportBaseView(ConfirmView):
    object_permission = permission_events_export

    def get_extra_context(self):
        return {
            'message': _(
                'The process will be performed in the background. '
                'The exported events will be available in the downloads area.'
            )
        }

    def view_action(self):
        decomposed_queryset = QuerysetParametersSerializer.decompose(
            _model=Action, **self.get_queryset_parameters()
        )

        task_event_queryset_export.apply_async(
            kwargs={
                'decomposed_queryset': decomposed_queryset,
                'user_id': self.request.user.pk
            }
        )

        messages.success(
            request=self.request, message=_(
                'Event list export task queued successfully.'
            )
        )


class EventListExportView(EventExportBaseView):
    object_permission = permission_events_export

    def get_extra_context(self):
        context = super().get_extra_context()
        context.update(
            {
                'title': _('Export events'),
            }
        )
        return context

    def get_queryset_parameters(self):
        return {
            '_method_name': 'all'
        }


class ObjectEventExportView(
    ExternalContentTypeObjectViewMixin, EventExportBaseView
):
    def get_extra_context(self):
        context = super().get_extra_context()
        context.update(
            {
                'object': self.external_object,
                'title': _('Export events for: %s') % self.external_object,
            }
        )
        return context

    def get_queryset_parameters(self):
        return {
            '_method_name': 'any', 'obj': self.external_object
        }


class CurrentUserEventExportView(ObjectEventExportView):
    object_permission = permission_events_export

    def get_external_object(self):
        return self.request.user

    def get_queryset_parameters(self):
        return {
            '_method_name': 'actor', 'obj': self.external_object
        }


class VerbEventExportView(EventExportBaseView):
    def get_extra_context(self):
        context = super().get_extra_context()
        context.update(
            {
                'title': _(
                    'Events of type: %s'
                ) % EventType.get(name=self.kwargs['verb']),
            }
        )
        return context

    def get_queryset_parameters(self):
        return {
            '_method_name': 'filter', 'verb': self.kwargs['verb']
        }
