from __future__ import absolute_import, unicode_literals

from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from actstream.models import Action, any_stream

from acls.models import AccessControlList
from common.generics import FormView, SimpleView
from common.utils import encapsulate
from common.views import SingleObjectListView

from .classes import EventType, ModelEventType
from .forms import (
    EventTypeUserRelationshipFormSet, ObjectEventTypeUserRelationshipFormSet
)
from .models import StoredEventType
from .permissions import permission_events_view
from .widgets import event_object_link


class EventListView(SingleObjectListView):
    view_permission = permission_events_view

    def get_queryset(self):
        return Action.objects.all()

    def get_extra_context(self):
        return {
            'extra_columns': (
                {
                    'name': _('Target'),
                    'attribute': encapsulate(
                        lambda entry: event_object_link(entry)
                    )
                },
            ),
            'hide_object': True,
            'title': _('Events'),
        }


class EventTypeSubscriptionListView(FormView):
    form_class = EventTypeUserRelationshipFormSet
    main_model = 'user'
    submodel = StoredEventType

    def dispatch(self, *args, **kwargs):
        EventType.refresh()
        return super(EventTypeSubscriptionListView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        try:
            for instance in form:
                instance.save()
        except Exception as exception:
            messages.error(
                self.request,
                _('Error updating event subscription; %s') % exception
            )
        else:
            messages.success(
                self.request, _('Event subscriptions updated successfully')
            )

        return super(
            EventTypeSubscriptionListView, self
        ).form_valid(form=form)

    def get_object(self):
        return self.request.user

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

    def get_post_action_redirect(self):
        return reverse('common:current_user_details')

    def get_queryset(self):
        # Return the queryset by name from the sorted list of the class
        event_type_ids = [event_type.id for event_type in EventType.all()]
        return self.submodel.objects.filter(name__in=event_type_ids)


class NotificationListView(SingleObjectListView):
    def get_queryset(self):
        return self.request.user.notifications.all()

    def get_extra_context(self):
        return {
            'hide_object': True,
            'object': self.request.user,
            'title': _('Notifications'),
        }


class NotificationMarkRead(SimpleView):
    def dispatch(self, *args, **kwargs):
        self.get_queryset().filter(pk=self.kwargs['pk']).update(read=True)
        return HttpResponseRedirect(reverse('events:user_notifications_list'))

    def get_queryset(self):
        return self.request.user.notifications.all()


class NotificationMarkReadAll(SimpleView):
    def dispatch(self, *args, **kwargs):
        self.get_queryset().update(read=True)
        return HttpResponseRedirect(reverse('events:user_notifications_list'))

    def get_queryset(self):
        return self.request.user.notifications.all()


class ObjectEventListView(EventListView):
    view_permissions = None

    def dispatch(self, request, *args, **kwargs):
        self.object_content_type = get_object_or_404(
            ContentType, app_label=self.kwargs['app_label'],
            model=self.kwargs['model']
        )

        try:
            self.content_object = self.object_content_type.get_object_for_this_type(
                pk=self.kwargs['object_id']
            )
        except self.object_content_type.model_class().DoesNotExist:
            raise Http404

        AccessControlList.objects.check_access(
            permissions=permission_events_view, user=request.user,
            obj=self.content_object
        )

        return super(
            ObjectEventListView, self
        ).dispatch(request, *args, **kwargs)

    def get_extra_context(self):
        return {
            'hide_object': True,
            'object': self.content_object,
            'title': _('Events for: %s') % self.content_object,
        }

    def get_queryset(self):
        return any_stream(self.content_object)


class ObjectEventTypeSubscriptionListView(FormView):
    form_class = ObjectEventTypeUserRelationshipFormSet

    def dispatch(self, *args, **kwargs):
        EventType.refresh()
        return super(ObjectEventTypeSubscriptionListView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        try:
            for instance in form:
                instance.save()
        except Exception as exception:
            messages.error(
                self.request,
                _('Error updating object event subscription; %s') % exception
            )
        else:
            messages.success(
                self.request, _('Object event subscriptions updated successfully')
            )

        return super(
            ObjectEventTypeSubscriptionListView, self
        ).form_valid(form=form)

    def get_object(self):
        object_content_type = get_object_or_404(
            ContentType, app_label=self.kwargs['app_label'],
            model=self.kwargs['model']
        )

        try:
            content_object = object_content_type.get_object_for_this_type(
                pk=self.kwargs['object_id']
            )
        except object_content_type.model_class().DoesNotExist:
            raise Http404

        AccessControlList.objects.check_access(
            permissions=permission_events_view, user=self.request.user,
            obj=content_object
        )

        return content_object

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
            initial.append({
                'user': self.request.user,
                'object': obj,
                'stored_event_type': element,
            })
        return initial

    def get_queryset(self):
        return ModelEventType.get_for_instance(instance=self.get_object())


class VerbEventListView(SingleObjectListView):
    def get_queryset(self):
        return Action.objects.filter(verb=self.kwargs['verb'])

    def get_extra_context(self):
        return {
            'extra_columns': (
                {
                    'name': _('Target'),
                    'attribute': encapsulate(
                        lambda entry: event_object_link(entry)
                    )
                },
            ),
            'hide_object': True,
            'title': _(
                'Events of type: %s'
            ) % EventType.get(name=self.kwargs['verb']),
        }
