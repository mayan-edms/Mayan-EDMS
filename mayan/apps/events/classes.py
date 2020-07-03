import json
import logging

from django.apps import apps
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _

from actstream import action

from mayan.apps.templating.classes import Template

from .permissions import permission_events_view

logger = logging.getLogger(name=__name__)


class EventModelRegistry:
    @staticmethod
    def register(model):
        from actstream import registry
        registry.register(model)


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
        return force_text(self.label)

    def add_event_type(self, **kwargs):
        event_type = EventType(namespace=self, **kwargs)
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
            # cache
            event_type.stored_event_type = None
            event_type.get_stored_event_type()

    def __init__(self, namespace, label, name, extra_data_template_name=None):
        self.extra_data_template_name = extra_data_template_name
        self.label = label
        self.name = name
        self.namespace = namespace
        self.stored_event_type = None
        if extra_data_template_name:
            self.template = Template(template_name=extra_data_template_name)
        else:
            self.template = None
        self.__class__._registry[self.id] = self

    def __str__(self):
        return force_text('{}: {}'.format(self.namespace.label, self.label))

    def commit(self, actor=None, action_object=None, target=None, extra_data=None):
        extra_data = extra_data or {}

        AccessControlList = apps.get_model(
            app_label='acls', model_name='AccessControlList'
        )
        Action = apps.get_model(
            app_label='actstream', model_name='Action'
        )
        ActionExtraData = apps.get_model(
            app_label='events', model_name='ActionExtraData'
        )
        ContentType = apps.get_model(
            app_label='contenttypes', model_name='ContentType'
        )
        Notification = apps.get_model(
            app_label='events', model_name='Notification'
        )

        results = action.send(
            actor or target, actor=actor, verb=self.id,
            action_object=action_object, target=target
        )

        for handler, result in results:
            if isinstance(result, Action):
                ActionExtraData.objects.create(
                    action=result, data=json.dumps(extra_data)
                )

                for user in get_user_model().objects.all():
                    notification = None

                    if user.event_subscriptions.filter(stored_event_type__name=result.verb).exists():
                        if result.target:
                            try:
                                AccessControlList.objects.check_access(
                                    obj=result.target,
                                    permissions=(permission_events_view,),
                                    user=user
                                )
                            except PermissionDenied:
                                pass
                            else:
                                notification, created = Notification.objects.get_or_create(
                                    action=result, user=user
                                )
                        else:
                            notification, created = Notification.objects.get_or_create(
                                action=result, user=user
                            )

                    if result.target:
                        content_type = ContentType.objects.get_for_model(model=result.target)

                        relationship = user.object_subscriptions.filter(
                            content_type=content_type,
                            object_id=result.target.pk,
                            stored_event_type__name=result.verb
                        )

                        if relationship.exists():
                            try:
                                AccessControlList.objects.check_access(
                                    obj=result.target,
                                    permissions=(permission_events_view,),
                                    user=user
                                )
                            except PermissionDenied:
                                pass
                            else:
                                notification, created = Notification.objects.get_or_create(
                                    action=result, user=user
                                )

                    if not notification and result.action_object:
                        content_type = ContentType.objects.get_for_model(model=result.action_object)

                        relationship = user.object_subscriptions.filter(
                            content_type=content_type,
                            object_id=result.action_object.pk,
                            stored_event_type__name=result.verb
                        )

                        if relationship.exists():
                            try:
                                AccessControlList.objects.check_access(
                                    obj=result.action_object,
                                    permissions=(permission_events_view,),
                                    user=user
                                )
                            except PermissionDenied:
                                pass
                            else:
                                notification, created = Notification.objects.get_or_create(
                                    action=result, user=user
                                )

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
