from django.utils.translation import ugettext_lazy as _

from actstream.models import Action, any_stream

from mayan.apps.views.generics import SingleObjectListView
from mayan.apps.views.mixins import ExternalContentTypeObjectViewMixin

from ..icons import icon_events_list
from ..permissions import permission_events_view

from .mixins import EventViewMixin

__all__ = (
    'EventListView', 'ObjectEventListView', 'VerbEventListView'
)


class EventListBaseView(SingleObjectListView):
    object_permission = permission_events_view

    def get_extra_context(self):
        return {
            'hide_object': True,
            'no_results_icon': icon_events_list,
            'no_results_text': _(
                'Events track actions that have been performed on, to, '
                'or with objects.'
            ),
            'no_results_title': _('There are no events'),
            'title': _('Events')
        }


class EventListView(EventListBaseView):
    def get_source_queryset(self):
        return Action.objects.all()


class ObjectEventListView(ExternalContentTypeObjectViewMixin, EventListBaseView):
    def get_extra_context(self):
        context = super().get_extra_context()
        context.update(
            {
                'no_results_title': _('There are no events for this object'),
                'object': self.external_object,
                'title': _('Events for: %s') % self.external_object,
            }
        )
        return context

    def get_source_queryset(self):
        return any_stream(obj=self.external_object)


class VerbEventListView(EventViewMixin, EventListBaseView):
    def get_extra_context(self):
        context = super().get_extra_context()
        context.update(
            {
                'no_results_title': _('There are no events of this type'),
                'title': _(
                    'Events of type: %s'
                ) % self.get_event_type(id=self.kwargs['verb'])
            }
        )
        return context

    def get_source_queryset(self):
        return Action.objects.filter(verb=self.kwargs['verb'])
