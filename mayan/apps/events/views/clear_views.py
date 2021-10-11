from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

from actstream.models import Action

from mayan.apps.common.classes import QuerysetParametersSerializer
from mayan.apps.views.generics import ConfirmView
from mayan.apps.views.mixins import ExternalContentTypeObjectViewMixin

from ..classes import EventType
from ..permissions import permission_events_clear
from ..tasks import task_event_queryset_clear

__all__ = (
    'CurrentUserEventClearView', 'EventListClearView',
    'ObjectEventClearView', 'VerbEventClearView'
)


class EventClearBaseView(ConfirmView):
    object_permission = permission_events_clear

    def get_extra_context(self):
        return {
            'message': _(
                'This action is not reversible. The process will be performed '
                'in the background. '
            )
        }

    def get_task_extra_kwargs(self):
        return {}

    def view_action(self):
        decomposed_queryset = QuerysetParametersSerializer.decompose(
            _model=Action, **self.get_queryset_parameters()
        )

        task_kwargs = {
            'decomposed_queryset': decomposed_queryset,
            'user_id': self.request.user.pk
        }

        task_kwargs.update(self.get_task_extra_kwargs())

        task_event_queryset_clear.apply_async(kwargs=task_kwargs)

        messages.success(
            request=self.request, message=_(
                'Event list clear task queued successfully.'
            )
        )


class EventListClearView(EventClearBaseView):
    object_permission = permission_events_clear

    def get_extra_context(self):
        context = super().get_extra_context()
        context.update(
            {
                'title': _('Clear events'),
            }
        )
        return context

    def get_queryset_parameters(self):
        return {
            '_method_name': 'all'
        }


class ObjectEventClearView(
    ExternalContentTypeObjectViewMixin, EventClearBaseView
):
    def get_extra_context(self):
        context = super().get_extra_context()
        context.update(
            {
                'object': self.external_object,
                'title': _('Clear events of: %s') % self.external_object,
            }
        )
        return context

    def get_queryset_parameters(self):
        return {
            '_method_name': 'any', 'obj': self.external_object
        }

    def get_task_extra_kwargs(self):
        return {
            'target_content_type_id': self.external_object_content_type.pk,
            'target_object_id': self.external_object.pk
        }


class CurrentUserEventClearView(ObjectEventClearView):
    object_permission = permission_events_clear

    def get_external_object(self):
        return self.request.user

    def get_queryset_parameters(self):
        return {
            '_method_name': 'actor', 'obj': self.external_object
        }

    def get_task_extra_kwargs(self):
        return {}


class VerbEventClearView(EventClearBaseView):
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
