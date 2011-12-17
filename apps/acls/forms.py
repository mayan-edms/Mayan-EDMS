from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, Group

from permissions.models import Permission, Role
from common.utils import generate_choices_w_labels, encapsulate, get_object_name

from acls.models import AccessHolder


class HolderSelectionForm(forms.Form):
    holder_gid = forms.ChoiceField(
        label=_(u'New holder')
    )
    
    def __init__(self, *args, **kwargs):
        staff_users = User.objects.filter(is_staff=True)
        super_users = User.objects.filter(is_superuser=True)
        #users = set(User.objects.exclude(pk__in=[member.pk for member in get_role_members(role)])) - set(staff_users) - set(super_users)
        users = set(User.objects.filter(is_active=True)) - set(staff_users) - set(super_users)
        roles = set(Role.objects.all())
        #groups = set(Group.objects.exclude(pk__in=[member.pk for member in get_role_members(role)]))
        groups = set(Group.objects.all())
        holder_list = list(users | groups | roles)
        
        #holder_list = kwargs.pop('holder_list', None)
        super(HolderSelectionForm, self).__init__(*args, **kwargs)
        #if holder_list:
        self.fields['holder_gid'].choices = [(AccessHolder.encapsulate(holder).gid, get_object_name(holder)) for holder in holder_list]


'''
def get_role_members(role):
    user_ct = ContentType.objects.get(model='user')
    group_ct = ContentType.objects.get(model='group')
    return [member.member_object for member in role.rolemember_set.filter(member_type__in=[user_ct, group_ct])]


def get_non_role_members(role):
    #non members = all users - members - staff - super users
    staff_users = User.objects.filter(is_staff=True)
    super_users = User.objects.filter(is_superuser=True)
    users = set(User.objects.exclude(pk__in=[member.pk for member in get_role_members(role)])) - set(staff_users) - set(super_users)
    groups = set(Group.objects.exclude(pk__in=[member.pk for member in get_role_members(role)]))
    return list(users | groups)


def add_role_member(role, selection):
    model, pk = selection.split(u',')
    ct = ContentType.objects.get(model=model)
    new_member, created = RoleMember.objects.get_or_create(role=role, member_type=ct, member_id=pk)
    if not created:
        raise Exception


def remove_role_member(role, selection):
    model, pk = selection.split(u',')
    ct = ContentType.objects.get(model=model)
    member = RoleMember.objects.get(role=role, member_type=ct, member_id=pk)
    member.delete()

def role_members(request, role_id):
    check_permissions(request.user, [PERMISSION_ROLE_EDIT])
    role = get_object_or_404(Role, pk=role_id)

    return assign_remove(
        request,
        left_list=lambda: generate_choices_w_labels(get_non_role_members(role)),
        right_list=lambda: generate_choices_w_labels(get_role_members(role)),
        add_method=lambda x: add_role_member(role, x),
        remove_method=lambda x: remove_role_member(role, x),
        left_list_title=_(u'non members of role: %s') % role,
        right_list_title=_(u'members of role: %s') % role,
        extra_context={
            'object': role,
            'object_name': _(u'role'),
        }
    )
'''
