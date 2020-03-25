from django.db import transaction

from mayan.apps.user_management.events import event_group_edited

from .events import event_role_edited


def method_group_roles_add(self, queryset, _user):
    with transaction.atomic():
        event_group_edited.commit(
            actor=_user, target=self
        )
        for role in queryset:
            self.roles.add(role)
            event_role_edited.commit(
                actor=_user, action_object=self, target=role
            )


def method_group_roles_remove(self, queryset, _user):
    with transaction.atomic():
        event_group_edited.commit(
            actor=_user, target=self
        )
        for role in queryset:
            self.roles.remove(role)
            event_role_edited.commit(
                actor=_user, action_object=self, target=role
            )
