from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from mayan.apps.acls.models import AccessControlList
from mayan.apps.views.generics import FormView

from ..classes import EventType, ModelEventType
from ..forms import (
    EventTypeUserRelationshipFormSet, ObjectEventTypeUserRelationshipFormSet
)
from ..models import StoredEventType
from ..permissions import permission_events_view

__all__ = (
    'EventTypeSubscriptionListView', 'ObjectEventTypeSubscriptionListView'
)


class EventTypeSubscriptionListView(FormView):
    form_class = EventTypeUserRelationshipFormSet
    main_model = 'user'
    submodel = StoredEventType

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
            initial.append({
                'user': obj,
                'main_model': self.main_model,
                'stored_event_type': element,
            })
        return initial

    def get_object(self):
        return self.request.user

    def get_post_action_redirect(self):
        return reverse(viewname='user_management:current_user_details')

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
            when_list.append(models.When(name=event_type_id, then=sort_index))

        queryset = self.submodel.objects.filter(name__in=event_type_ids)
        queryset = queryset.annotate(
            sort_index=models.Case(
                *when_list, output_field=models.IntegerField()
            )
        )
        return queryset.order_by('sort_index')


class ObjectEventTypeSubscriptionListView(FormView):
    form_class = ObjectEventTypeUserRelationshipFormSet

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
            'object': self.get_object(),
            'title': _(
                'Event subscriptions for: %s'
            ) % self.get_object()
        }

    def get_initial(self):
        obj = self.get_object()
        initial = []

        for element in self.get_queryset():
            initial.append(
                {
                    'user': self.request.user,
                    'object': obj,
                    'stored_event_type': element,
                }
            )
        return initial

    def get_object(self):
        object_content_type = get_object_or_404(
            klass=ContentType, app_label=self.kwargs['app_label'],
            model=self.kwargs['model_name']
        )

        try:
            content_object = object_content_type.get_object_for_this_type(
                pk=self.kwargs['object_id']
            )
        except object_content_type.model_class().DoesNotExist:
            raise Http404

        AccessControlList.objects.check_access(
            obj=content_object, permissions=(permission_events_view,),
            user=self.request.user
        )

        return content_object

    def get_queryset(self):
        return ModelEventType.get_for_instance(instance=self.get_object())
