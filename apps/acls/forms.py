from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, Group

from permissions.models import Permission, Role
from common.utils import generate_choices_w_labels, encapsulate, get_object_name

from acls.models import AccessHolder


class HolderSelectionForm(forms.Form):
    holder_gid = forms.ChoiceField(
        label=_(u'Holder')
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

