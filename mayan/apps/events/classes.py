import csv
import logging

from furl import furl

from django.apps import apps
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _

from actstream import action

from mayan.apps.common.menus import menu_list_facet
from mayan.apps.common.settings import setting_project_url
from mayan.apps.common.utils import return_attrib

from .literals import (
    DEFAULT_EVENT_LIST_EXPORT_FILENAME, EVENT_MANAGER_ORDER_AFTER
)
from .links import (
    link_events_for_object, link_object_event_types_user_subcriptions_list
)
from .permissions import permission_events_export, permission_events_view

logger = logging.getLogger(name=__name__)


DEFAULT_ACTION_EXPORTER_FIELD_NAMES = (
    'timestamp', 'id', 'actor_content_type', 'actor_object_id', 'actor',
    'target_content_type', 'target_object_id', 'target', 'verb',
    'action_object_content_type', 'action_object_object_id', 'action_object'
)


class ActionExporter:
    def __init__(self, queryset, field_names=None):
        self.field_names = field_names or DEFAULT_ACTION_EXPORTER_FIELD_NAMES
        self.queryset = queryset

    def export(self, file_object, user=None):
        AccessControlList = apps.get_model(
            app_label='acls', model_name='AccessControlList'
        )
        if user:
            self.queryset = AccessControlList.objects.restrict_queryset(
                queryset=self.queryset,
                permission=permission_events_export,
                user=user
            )

        writer = csv.writer(
            file_object, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL
        )
        file_object.write(','.join(self.field_names + ('\n',)))

        for entry in self.queryset.iterator():
            row = [
                str(
                    getattr(entry, field_name)
                ) for field_name in self.field_names
            ]
            writer.writerow(row)

    def export_to_download_file(self, user=None):
        # Avoid circular import
        from .events import event_events_exported

        DownloadFile = apps.get_model(
            app_label='storage', model_name='DownloadFile'
        )
        Message = apps.get_model(
            app_label='messaging', model_name='Message'
        )

        download_file = DownloadFile(
            filename=DEFAULT_EVENT_LIST_EXPORT_FILENAME,
            label=_('Event list export to CSV'),
            permission=permission_events_export.stored_permission
        )
        download_file._event_actor = user
        download_file.save()

        with download_file.open(mode='w') as file_object:
            self.export(file_object=file_object, user=user)

        event_events_exported.commit(
            actor=user, target=download_file
        )

        if user:
            download_list_url = furl(setting_project_url.value).join(
                reverse(
                    viewname='storage:download_file_list'
                )
            ).tostr()
            download_url = furl(setting_project_url.value).join(
                reverse(
                    viewname='storage:download_file_download',
                    kwargs={'download_file_id': download_file.pk}
                )
            ).tostr()

            Message.objects.create(
                sender_object=download_file,
                user=user,
                subject=_('Events exported.'),
                body=_(
                    'The event list has been exported and is available '
                    'for download using the link: %(download_url)s or from '
                    'the downloads area (%(download_list_url)s).'
                ) % {
                    'download_list_url': download_list_url,
                    'download_url': download_url,
                }
            )


class EventManager:
    EVENT_ATTRIBUTES = ('ignore', 'keep_attributes',)
    EVENT_ARGUMENTS = ('actor', 'action_object', 'target')

    def __init__(self, instance, **kwargs):
        self.instance = instance
        self.instance_event_attributes = {}
        self.kwargs = kwargs

    def commit(self):
        if not self.instance_event_attributes['ignore']:
            self._commit()

    def get_event_arguments(self, argument_map):
        result = {}

        for argument in self.EVENT_ARGUMENTS:
            # Grab the static argument value from the argument map.
            # If the argument is not in the map, it is dynamic and must be
            # obtained from the instance attributes.
            value = argument_map.get(
                argument, self.instance_event_attributes[argument]
            )

            if value == 'self':
                result[argument] = self.instance
            elif isinstance(value, str):
                result[argument] = return_attrib(obj=self.instance, attrib=value)
            else:
                result[argument] = value

        return result

    def pop_event_attributes(self):
        for attribute in self.EVENT_ATTRIBUTES:
            # If the attribute is not set or is set but is None.
            if not self.instance_event_attributes.get(attribute, None):
                full_name = '_event_{}'.format(attribute)
                value = self.instance.__dict__.pop(full_name, None)
                self.instance_event_attributes[attribute] = value

        keep_attributes = self.instance_event_attributes['keep_attributes'] or ()

        for attribute in self.EVENT_ARGUMENTS:
            # If the attribute is not set or is set but is None.
            if not self.instance_event_attributes.get(attribute, None):
                full_name = '_event_{}'.format(attribute)
                if full_name in keep_attributes:
                    value = self.instance.__dict__.get(full_name, None)
                else:
                    value = self.instance.__dict__.pop(full_name, None)

                self.instance_event_attributes[attribute] = value

    def prepare(self):
        """Optional method to gather information before the actual commit"""


class EventManagerMethodAfter(EventManager):
    order = EVENT_MANAGER_ORDER_AFTER

    def _commit(self):
        self.kwargs['event'].commit(
            **self.get_event_arguments(argument_map=self.kwargs)
        )


class EventManagerSave(EventManager):
    order = EVENT_MANAGER_ORDER_AFTER

    def _commit(self):
        if self.created:
            if 'created' in self.kwargs:
                self.kwargs['created']['event'].commit(
                    **self.get_event_arguments(argument_map=self.kwargs['created'])
                )
        else:
            if 'edited' in self.kwargs:
                self.kwargs['edited']['event'].commit(
                    **self.get_event_arguments(argument_map=self.kwargs['edited'])
                )

    def prepare(self):
        self.created = not self.instance.pk


class EventModelRegistry:
    @staticmethod
    def register(model, bind_links=True, menu=None):
        from actstream import registry
        registry.register(model)

        if bind_links:
            menu = menu or menu_list_facet

            menu.bind_links(
                links=(
                    link_events_for_object,
                    link_object_event_types_user_subcriptions_list
                ), sources=(model,)
            )


class EventTypeNamespace:
    _registry = {}

    @classmethod
    def all(cls):
        return sorted(cls._registry.values())

    @classmethod
    def get(cls, name):
        return cls._registry[name]

    def __init__(self, name, label):
        self.name = name
        self.label = label
        self.event_types = []
        self.__class__._registry[name] = self

    def __lt__(self, other):
        return self.label < other.label

    def __str__(self):
        return force_text(s=self.label)

    def add_event_type(self, name, label):
        event_type = EventType(namespace=self, name=name, label=label)
        self.event_types.append(event_type)
        return event_type

    def get_event_types(self):
        return EventType.sort(event_type_list=self.event_types)


class EventType:
    _registry = {}

    @staticmethod
    def sort(event_type_list):
        return sorted(
            event_type_list, key=lambda x: (x.namespace.label, x.label)
        )

    @classmethod
    def all(cls):
        # Return sorted permisions by namespace.name
        return EventType.sort(event_type_list=cls._registry.values())

    @classmethod
    def get(cls, name):
        try:
            return cls._registry[name]
        except KeyError:
            return _('Unknown or obsolete event type: %s') % name

    @classmethod
    def refresh(cls):
        for event_type in cls.all():
            # Invalidate cache and recreate store events while repopulating
            # cache.
            event_type.stored_event_type = None
            event_type.get_stored_event_type()

    def __init__(self, namespace, name, label):
        self.namespace = namespace
        self.name = name
        self.label = label
        self.stored_event_type = None
        self.__class__._registry[self.id] = self

    def __str__(self):
        return '{}: {}'.format(self.namespace.label, self.label)

    def commit(self, actor=None, action_object=None, target=None):
        AccessControlList = apps.get_model(
            app_label='acls', model_name='AccessControlList'
        )
        EventSubscription = apps.get_model(
            app_label='events', model_name='EventSubscription'
        )
        Notification = apps.get_model(
            app_label='events', model_name='Notification'
        )
        ObjectEventSubscription = apps.get_model(
            app_label='events', model_name='ObjectEventSubscription'
        )
        User = get_user_model()

        if actor is None and target is None:
            # If the actor and the target are None there is no way to
            # create a new event.
            logger.warning(
                'Attempting to commit event "%s" without an actor or a '
                'target. This is not yet supported.', self
            )
            return

        result = action.send(
            actor or target, actor=actor, verb=self.id,
            action_object=action_object, target=target
        )[0][1]
        # The [0][1] means: get the first and only action from the list
        # and ignore the handler.

        # Create notifications for the actions created by the event committed.

        # Gather the users subscribed globally to the event.
        user_queryset = User.objects.filter(
            id__in=EventSubscription.objects.filter(
                stored_event_type__name=result.verb
            ).values('user')
        )

        # Gather the users subscribed to the target object event.
        if result.target:
            user_queryset = user_queryset | User.objects.filter(
                id__in=ObjectEventSubscription.objects.filter(
                    content_type=result.target_content_type,
                    object_id=result.target.pk,
                    stored_event_type__name=result.verb
                ).values('user')
            )

        # Gather the users subscribed to the action object event.
        if result.action_object:
            user_queryset = user_queryset | User.objects.filter(
                id__in=ObjectEventSubscription.objects.filter(
                    content_type=result.action_object_content_type,
                    object_id=result.action_object.pk,
                    stored_event_type__name=result.verb
                ).values('user')
            )

        for user in user_queryset:
            if result.target:
                try:
                    AccessControlList.objects.check_access(
                        obj=result.target,
                        permissions=(permission_events_view,),
                        user=user
                    )
                except PermissionDenied:
                    """
                    User is subscribed to the event but does
                    not have permissions for the event's target.
                    """
                else:
                    Notification.objects.create(action=result, user=user)
                    # Don't check or add any other notification for the
                    # same user-event-object.
                    continue

            if result.action_object:
                try:
                    AccessControlList.objects.check_access(
                        obj=result.action_object,
                        permissions=(permission_events_view,),
                        user=user
                    )
                except PermissionDenied:
                    """
                    User is subscribed to the event but does
                    not have permissions for the event's action_object.
                    """
                else:
                    Notification.objects.create(action=result, user=user)
                    # Don't check or add any other notification for the
                    # same user-event-object.
                    continue

        return result

    def get_stored_event_type(self):
        if not self.stored_event_type:
            StoredEventType = apps.get_model(
                app_label='events', model_name='StoredEventType'
            )

            self.stored_event_type, created = StoredEventType.objects.get_or_create(
                name=self.id
            )

        return self.stored_event_type

    @property
    def id(self):
        return '%s.%s' % (self.namespace.name, self.name)


class ModelEventType:
    """
    Class to allow matching a model to a specific set of events.
    """
    _inheritances = {}
    _registry = {}

    @classmethod
    def get_for_class(cls, klass):
        return cls._registry.get(klass, ())

    @classmethod
    def get_for_instance(cls, instance):
        StoredEventType = apps.get_model(
            app_label='events', model_name='StoredEventType'
        )

        events = []

        class_events = cls._registry.get(type(instance))

        if class_events:
            events.extend(class_events)

        pks = [
            event.id for event in set(events)
        ]

        return EventType.sort(
            event_type_list=StoredEventType.objects.filter(name__in=pks)
        )

    @classmethod
    def get_inheritance(cls, model):
        return cls._inheritances[model]

    @classmethod
    def register(cls, model, event_types):
        cls._registry.setdefault(model, [])
        for event_type in event_types:
            cls._registry[model].append(event_type)

    @classmethod
    def register_inheritance(cls, model, related):
        cls._inheritances[model] = related
