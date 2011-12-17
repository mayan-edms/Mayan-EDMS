from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, Group

from permissions.models import Permission, Role
from common.utils import generate_choices_w_labels, encapsulate, get_object_name

from acls.models import AccessHolder


def _as_choice_list(holders):
    return sorted([(AccessHolder.encapsulate(holder).gid, get_object_name(holder, display_object_type=False)) for holder in holders], key=lambda x: x[1])

class HolderSelectionForm(forms.Form):
    holder_gid = forms.ChoiceField(
        label=_(u'New holder')
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
        
        non_holder_list = []
        if users:
            non_holder_list.append((_(u'Users'), _as_choice_list(list(users))))
            
        if groups:
            non_holder_list.append((_(u'Groups'), _as_choice_list(list(groups))))
            
        if roles:
            non_holder_list.append((_(u'Roles'), _as_choice_list(list(roles))))

        super(HolderSelectionForm, self).__init__(*args, **kwargs)
        self.fields['holder_gid'].choices = non_holder_list
