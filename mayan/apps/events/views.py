from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from actstream.models import Action, any_stream

from mayan.apps.acls.models import AccessControlList
from mayan.apps.views.generics import (
    FormView, SimpleView, SingleObjectListView
)

from .classes import EventType, ModelEventType
from .forms import (
    EventTypeUserRelationshipFormSet, ObjectEventTypeUserRelationshipFormSet
)
from .icons import (
    icon_events_list, icon_user_notifications_list
)
from .links import link_event_types_subscriptions_list
from .models import StoredEventType
from .permissions import permission_events_view


class EventListView(SingleObjectListView):
    view_permission = permission_events_view

    def get_extra_context(self):
        return {
            'hide_object': True,
            'title': _('Events'),
        }

    def get_source_queryset(self):
        return Action.objects.all()


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
                message=_(
                    'Error updating event subscription; %s'
                ) % exception, request=self.request
            )
        else:
            messages.success(
                message=_('Event subscriptions updated successfully'),
                request=self.request
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

    def get_queryset(self):
        # Return the queryset by name from the sorted list of the class
        event_type_ids = [event_type.id for event_type in EventType.all()]
        return self.submodel.objects.filter(name__in=event_type_ids)

    def get_post_action_redirect(self):
        return reverse(viewname='user_management:current_user_details')


class NotificationListView(SingleObjectListView):
    def get_extra_context(self):
        return {
            'hide_object': True,
            'no_results_icon': icon_user_notifications_list,
            'no_results_main_link': link_event_types_subscriptions_list.resolve(
                context=RequestContext(request=self.request)
            ),
            'no_results_text': _(
                'Subscribe to global or object events to receive '
                'notifications.'
            ),
            'no_results_title': _('There are no notifications'),
            'object': self.request.user,
            'title': _('Notifications'),
        }

    def get_source_queryset(self):
        return self.request.user.notifications.all()


class NotificationMarkRead(SimpleView):
    def dispatch(self, *args, **kwargs):
        self.get_queryset().filter(
            pk=self.kwargs['notification_id']
        ).update(read=True)
        return HttpResponseRedirect(
            redirect_to=reverse(viewname='events:user_notifications_list')
        )

    def get_queryset(self):
        return self.request.user.notifications.all()


class NotificationMarkReadAll(SimpleView):
    def dispatch(self, *args, **kwargs):
        self.get_queryset().update(read=True)
        return HttpResponseRedirect(
            redirect_to=reverse(viewname='events:user_notifications_list')
        )

    def get_queryset(self):
        return self.request.user.notifications.all()


class ObjectEventListView(EventListView):
    view_permission = None

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(
            ObjectEventListView, self
        ).dispatch(request, *args, **kwargs)

    def get_extra_context(self):
        context = super(ObjectEventListView, self).get_extra_context()
        context.update(
            {
                'hide_object': True,
                'no_results_icon': icon_events_list,
                'no_results_text': _(
                    'Events are actions that have been performed to this object '
                    'or using this object.'
                ),
                'no_results_title': _('There are no events for this object'),
                'object': self.object,
                'title': _('Events for: %s') % self.object,
            }
        )
        return context

    def get_object(self):
        content_type = get_object_or_404(
            klass=ContentType, app_label=self.kwargs['app_label'],
            model=self.kwargs['model_name']
        )

        queryset = AccessControlList.objects.restrict_queryset(
            permission=permission_events_view,
            queryset=content_type.model_class().objects.all(),
            user=self.request.user
        )
        return get_object_or_404(
            klass=queryset, pk=self.kwargs['object_id']
        )

    def get_source_queryset(self):
        return any_stream(obj=self.object)


class ObjectEventTypeSubscriptionListView(FormView):
    form_class = ObjectEventTypeUserRelationshipFormSet

    def dispatch(self, *args, **kwargs):
        EventType.refresh()
        return super(ObjectEventTypeSubscriptionListView, self).dispatch(
            *args, **kwargs
        )

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

        return super(
            ObjectEventTypeSubscriptionListView, self
        ).form_valid(form=form)

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

    def get_queryset(self):
        return ModelEventType.get_for_instance(instance=self.get_object())


class CurrentUserEventListView(ObjectEventListView):
    def get_object(self):
        return self.request.user


class VerbEventListView(SingleObjectListView):
    def get_extra_context(self):
        return {
            'hide_object': True,
            'title': _(
                'Events of type: %s'
            ) % EventType.get(name=self.kwargs['verb']),
        }

    def get_source_queryset(self):
        return Action.objects.filter(verb=self.kwargs['verb'])
