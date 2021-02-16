from django.utils.translation import ugettext_lazy as _

from actstream.models import Action, any_stream

from mayan.apps.acls.models import AccessControlList
from mayan.apps.views.generics import ConfirmView
from mayan.apps.views.mixins import ExternalContentTypeObjectViewMixin

from ..classes import ActionExporter, EventType
from ..permissions import permission_events_export

__all__ = (
    'CurrentUserEventExportView', 'EventListExportView',
    'ObjectEventExportView', 'VerbEventExportView'
)

#TODO Add event export permission


class EventExportBaseView(ConfirmView):
    object_permission = permission_events_export

    def get_queryset(self):
        return AccessControlList.objects.restrict_queryset(
            queryset=self.get_source_queryset(),
            permission=permission_events_export,
            user=self.request.user
        )

    def view_action(self):
        ActionExporter(queryset=self.get_queryset()).export()


class EventListExportView(EventExportBaseView):
    object_permission = permission_events_export

    def get_extra_context(self):
        return {
            'title': _('Export events'),
        }

    def get_source_queryset(self):
        return Action.objects.all()


class ObjectEventExportView(
    ExternalContentTypeObjectViewMixin, EventExportBaseView
):
    def get_extra_context(self):
        return {
            'object': self.external_object,
            'title': _('Export events for: %s') % self.external_object,
        }

    def get_source_queryset(self):
        return any_stream(obj=self.external_object)


class CurrentUserEventExportView(ObjectEventExportView):
    object_permission = permission_events_export

    def get_external_object(self):
        return self.request.user


class VerbEventExportView(EventExportBaseView):
    def get_extra_context(self):
        return {
            #'hide_object': True,
            'title': _(
                'Events of type: %s'
            ) % EventType.get(name=self.kwargs['verb']),
        }

    def get_source_queryset(self):
        return Action.objects.filter(verb=self.kwargs['verb'])
