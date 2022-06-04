from django.contrib import messages
from django.db import models
from django.utils.translation import ugettext_lazy as _

from mayan.apps.views.generics import FormView, SingleObjectListView
from mayan.apps.views.mixins import ExternalContentTypeObjectViewMixin

from ..classes import EventType, ModelEventType
from ..forms import (
    EventTypeUserRelationshipFormSet, ObjectEventTypeUserRelationshipFormSet
)
from ..icons import (
    icon_event_types_subscriptions_list,
    icon_object_event_type_user_subscription_list,
    icon_user_object_subscriptions_list
)
from ..models import ObjectEventSubscription, StoredEventType
from ..permissions import permission_events_view


class EventTypeSubscriptionListView(FormView):
    form_class = EventTypeUserRelationshipFormSet
    main_model = 'user'
    submodel = StoredEventType
    view_icon = icon_event_types_subscriptions_list

    def dispatch(self, *args, **kwargs):
        EventType.refresh()
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        try:
            for instance in form:
                instance.save()
        except Exception as exception:
            messages.error(
                message=_(
                    'Error updating event subscription; %s'
                ) % exception, request=self.request
            )
        else:
            messages.success(
                message=_('Event subscriptions updated successfully'),
                request=self.request
            )

        return super().form_valid(form=form)

    def get_extra_context(self):
        return {
            'form_display_mode_table': True,
            'object': self.get_object(),
            'title': _(
                'Event subscriptions'
            ) % self.get_object()
        }

    def get_initial(self):
        obj = self.get_object()
        initial = []

        for element in self.get_queryset():
            initial.append(
                {
                    'main_model': self.main_model,
                    'stored_event_type': element,
                    'user': obj
                }
            )
        return initial

    def get_object(self):
        return self.request.user

    def get_queryset(self):
        # Return the queryset by name from the sorted list of the class
        event_type_ids = [event_type.id for event_type in EventType.all()]

        # Preserve the queryset order to that of the sorted ID list by
        # namespace label and event label.
        # Create a conditional statement to annotate each row with the sort
        # index number. Then sort the query set by the custom sort index
        # field.
        when_list = []
        for sort_index, event_type_id in enumerate(iterable=event_type_ids):
            when_list.append(
                models.When(name=event_type_id, then=sort_index)
            )

        queryset = self.submodel.objects.filter(name__in=event_type_ids)
        queryset = queryset.annotate(
            sort_index=models.Case(
                *when_list, output_field=models.IntegerField()
            )
        )
        return queryset.order_by('sort_index')


class ObjectEventTypeSubscriptionListView(
    ExternalContentTypeObjectViewMixin, FormView
):
    external_object_permission = permission_events_view
    form_class = ObjectEventTypeUserRelationshipFormSet
    view_icon = icon_object_event_type_user_subscription_list

    def dispatch(self, *args, **kwargs):
        EventType.refresh()
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        try:
            for instance in form:
                instance.save()
        except Exception as exception:
            messages.error(
                message=_(
                    'Error updating object event subscription; %s'
                ) % exception, request=self.request
            )
        else:
            messages.success(
                message=_(
                    'Object event subscriptions updated successfully'
                ), request=self.request
            )

        return super().form_valid(form=form)

    def get_extra_context(self):
        return {
            'form_display_mode_table': True,
            'object': self.external_object,
            'title': _(
                'Event subscriptions for: %s'
            ) % self.external_object
        }

    def get_initial(self):
        initial = []

        for element in self.get_queryset():
            initial.append(
                {
                    'object': self.external_object,
                    'stored_event_type': element,
                    'user': self.request.user
                }
            )
        return initial

    def get_queryset(self):
        return ModelEventType.get_for_instance(instance=self.external_object)


class UserObjectSubscriptionList(SingleObjectListView):
    object_permission = permission_events_view
    view_icon = icon_user_object_subscriptions_list

    def get_extra_context(self):
        return {
            'hide_object': True,
            'no_results_icon': icon_user_object_subscriptions_list,
            'no_results_text': _(
                'Subscribe to the events of an object to received '
                'notifications when those events occur.'
            ),
            'no_results_title': _('There are no object event subscriptions'),
            'object': self.request.user,
            'title': _('Object event subscriptions')
        }

    def get_source_queryset(self):
        return ObjectEventSubscription.objects.filter(user=self.request.user)
