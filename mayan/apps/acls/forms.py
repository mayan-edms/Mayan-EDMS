from __future__ import absolute_import, unicode_literals

from django import forms
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext_lazy as _
from django.utils.functional import SimpleLazyObject

from common.models import AnonymousUserSingleton
from common.utils import get_object_name
from permissions.models import Role

from .classes import AccessHolder
from .models import CreatorSingleton

anonymous_singleton = SimpleLazyObject(lambda: AnonymousUserSingleton.objects.get())
creator_singleton = SimpleLazyObject(lambda: CreatorSingleton.objects.get())


def _as_choice_list(holders):
    return sorted([(AccessHolder.encapsulate(holder).gid, get_object_name(holder, display_object_type=False)) for holder in holders], key=lambda x: x[1])


class BaseHolderSelectionForm(forms.Form):
    holder_gid = forms.ChoiceField(
        label=_('New holder')
    )

    def __init__(self, *args, **kwargs):
        current_holders = kwargs.pop('current_holders', [])
        if current_holders:
            current_holders = [holder.source_object for holder in current_holders]

        staff_users = User.objects.filter(is_staff=True)
        super_users = User.objects.filter(is_superuser=True)
        users = set(User.objects.filter(is_active=True)) - set(staff_users) - set(super_users) - set(current_holders)
        roles = set(Role.objects.all()) - set(current_holders)
        groups = set(Group.objects.all()) - set(current_holders)
        special = set(self.special_holders) - set(current_holders)

        non_holder_list = []
        if users:
            non_holder_list.append((_('Users'), _as_choice_list(list(users))))

        if groups:
            non_holder_list.append((_('Groups'), _as_choice_list(list(groups))))

        if roles:
            non_holder_list.append((_('Roles'), _as_choice_list(list(roles))))

        if special:
            non_holder_list.append((_('Special'), _as_choice_list(list(special))))

        super(BaseHolderSelectionForm, self).__init__(*args, **kwargs)
        self.fields['holder_gid'].choices = non_holder_list


class HolderSelectionForm(BaseHolderSelectionForm):
    special_holders = [anonymous_singleton]


class ClassHolderSelectionForm(BaseHolderSelectionForm):
    special_holders = [anonymous_singleton, creator_singleton]
