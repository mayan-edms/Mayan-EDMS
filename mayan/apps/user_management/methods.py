from django.apps import apps
from django.contrib.auth import get_user_model
from django.shortcuts import reverse

from mayan.apps.events.classes import EventManagerSave
from mayan.apps.events.decorators import method_event

from .events import (
    event_group_created, event_group_edited, event_user_created,
    event_user_edited
)
from .permissions import permission_group_view, permission_user_view
from .querysets import get_user_queryset


def get_method_group_init():
    Group = apps.get_model(app_label='auth', model_name='Group')
    method_original = Group.__init__

    def method_init(self, *args, **kwargs):
        _instance_extra_data = kwargs.pop('_instance_extra_data', {})
        result = method_original(self, *args, **kwargs)
        for key, value in _instance_extra_data.items():
            setattr(self, key, value)

        return result

    return method_init


def get_method_group_save():
    Group = apps.get_model(app_label='auth', model_name='Group')
    group_save_original = Group.save

    @method_event(
        event_manager_class=EventManagerSave,
        created={
            'event': event_group_created,
            'target': 'self',
        },
        edited={
            'event': event_group_edited,
            'target': 'self',
        }
    )
    def method_group_save(self, *args, **kwargs):
        group_save_original(self, *args, **kwargs)

    return method_group_save


def method_group_get_users(self, user, permission=permission_user_view):
    AccessControlList = apps.get_model(
        app_label='acls', model_name='AccessControlList'
    )

    return AccessControlList.objects.restrict_queryset(
        permission=permission, queryset=get_user_queryset().filter(
            id__in=self.user_set.all()
        ), user=user
    )


def method_group_users_add(self, queryset, _event_actor=None):
    for user in queryset:
        self.user_set.add(user)
        event_group_edited.commit(
            action_object=user, actor=_event_actor or self._event_actor,
            target=self
        )


def method_group_users_remove(self, queryset, _event_actor=None):
    for user in queryset:
        self.user_set.remove(user)
        event_group_edited.commit(
            action_object=user, actor=_event_actor or self._event_actor,
            target=self
        )


def get_method_user_init():
    User = get_user_model()
    method_original = User.__init__

    def method_init(self, *args, **kwargs):
        _instance_extra_data = kwargs.pop('_instance_extra_data', {})
        result = method_original(self, *args, **kwargs)
        for key, value in _instance_extra_data.items():
            setattr(self, key, value)

        return result

    return method_init


def method_user_get_absolute_url(self):
    return reverse(
        viewname='user_management:user_details', kwargs={'user_id': self.pk}
    )


def method_user_get_groups(self, user, permission=permission_group_view):
    AccessControlList = apps.get_model(
        app_label='acls', model_name='AccessControlList'
    )

    return AccessControlList.objects.restrict_queryset(
        permission=permission, queryset=self.groups.all(), user=user
    )


def method_user_groups_add(self, queryset, _event_actor=None):
    for group in queryset:
        self.groups.add(group)
        event_user_edited.commit(
            action_object=group, actor=_event_actor or self._event_actor,
            target=self
        )


def method_user_groups_remove(self, queryset, _event_actor=None):
    for group in queryset:
        self.groups.remove(group)
        event_user_edited.commit(
            action_object=group, actor=_event_actor or self._event_actor,
            target=self
        )


def get_method_user_save():
    user_save_original = get_user_model().save

    @method_event(
        event_manager_class=EventManagerSave,
        created={
            'event': event_user_created,
            'target': 'self',
        },
        edited={
            'event': event_user_edited,
            'target': 'self',
        }
    )
    def method_user_save(self, *args, **kwargs):
        user_save_original(self, *args, **kwargs)

    return method_user_save
