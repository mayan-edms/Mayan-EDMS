from __future__ import unicode_literals

from django.contrib.auth.models import Group, User
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

from common.models import AnonymousUserSingleton
from common.utils import get_object_name

from .classes import Member


def _as_choice_list(items):
    return sorted([(Member.encapsulate(item).gid, get_object_name(item, display_object_type=False)) for item in items], key=lambda x: x[1])


def get_role_members(role, separate=False):
    user_ct = ContentType.objects.get(model='user')
    group_ct = ContentType.objects.get(model='group')
    anonymous = ContentType.objects.get(model='anonymoususersingleton')

    users = role.members(filter_dict={'member_type': user_ct})
    groups = role.members(filter_dict={'member_type': group_ct})
    anonymous = role.members(filter_dict={'member_type': anonymous})

    if separate:
        return users, groups, anonymous
    else:
        members = []

        if users:
            members.append((_('Users'), _as_choice_list(list(users))))

        if groups:
            members.append((_('Groups'), _as_choice_list(list(groups))))

        if anonymous:
            members.append((_('Special'), _as_choice_list(list(anonymous))))

        return members


def get_non_role_members(role):
    # non members = all users - members - staff - super users
    member_users, member_groups, member_anonymous = get_role_members(role, separate=True)

    staff_users = User.objects.filter(is_staff=True)
    super_users = User.objects.filter(is_superuser=True)

    users = set(User.objects.all()) - set(member_users) - set(staff_users) - set(super_users)
    groups = set(Group.objects.all()) - set(member_groups)
    anonymous = set([AnonymousUserSingleton.objects.get()]) - set(member_anonymous)

    non_members = []
    if users:
        non_members.append((_('Users'), _as_choice_list(list(users))))

    if groups:
        non_members.append((_('Groups'), _as_choice_list(list(groups))))

    if anonymous:
        non_members.append((_('Special'), _as_choice_list(list(anonymous))))

    return non_members
