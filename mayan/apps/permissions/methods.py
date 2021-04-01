from .events import event_role_edited


def method_group_roles_add(self, queryset, _event_actor=None):
    for role in queryset:
        self.roles.add(role)
        event_role_edited.commit(
            actor=_event_actor or self._event_actor, action_object=self,
            target=role
        )


def method_group_roles_remove(self, queryset, _event_actor=None):
    for role in queryset:
        self.roles.remove(role)
        event_role_edited.commit(
            actor=_event_actor or self._event_actor, action_object=self,
            target=role
        )
