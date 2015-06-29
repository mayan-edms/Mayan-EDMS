from __future__ import unicode_literals

import itertools
from json import loads
import operator

from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.conf import settings
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from common.views import (
    AssignRemoveView, SingleObjectCreateView, SingleObjectDeleteView,
    SingleObjectEditView
)
from common.utils import encapsulate
from common.widgets import two_state_template

from .classes import Permission, PermissionNamespace
from .forms import RoleForm, RoleForm_view
from .models import Role, StoredPermission
from .permissions import (
    permission_permission_grant, permission_permission_revoke,
    permission_role_view, permission_role_create, permission_role_delete,
    permission_role_edit
)


class RoleCreateView(SingleObjectCreateView):
    form_class = RoleForm
    model = Role
    view_permission = permission_role_create
    success_url = reverse_lazy('permissions:role_list')


class RoleDeleteView(SingleObjectDeleteView):
    model = Role
    view_permission = permission_role_delete
    success_url = reverse_lazy('permissions:role_list')


class RoleEditView(SingleObjectEditView):
    model = Role
    view_permission = permission_role_edit


class SetupRoleMembersView(AssignRemoveView):
    grouped = False

    def add(self, item):
        group = get_object_or_404(Group, pk=item)
        self.role.groups.add(group)

    def dispatch(self, request, *args, **kwargs):
        Permission.check_permissions(request.user, [permission_role_edit])
        self.role = get_object_or_404(Role, pk=self.kwargs['role_id'])
        self.left_list_title = _('Available groups')
        self.right_list_title = _('Member groups')

        return super(SetupRoleMembersView, self).dispatch(request, *args, **kwargs)

    def left_list(self):
        return [(unicode(group.pk), group.name) for group in set(Group.objects.all()) - set(self.role.groups.all())]

    def right_list(self):
        return [(unicode(group.pk), group.name) for group in self.role.groups.all()]

    def remove(self, item):
        group = get_object_or_404(Group, pk=item)
        self.role.groups.remove(group)

    def get_context_data(self, **kwargs):
        data = super(SetupRoleMembersView, self).get_context_data(**kwargs)
        data.update({
            'object': self.role,
            'title': _('Group members of role: %s') % self.role
        })

        return data


class SetupRolePermissionsView(AssignRemoveView):
    grouped = True

    @staticmethod
    def as_choice_list(items):
        return sorted([(item.pk, item) for item in items], key=lambda x: x[1])

    def add(self, item):
        permission = get_object_or_404(StoredPermission, pk=item)
        self.role.permissions.add(permission)

    def dispatch(self, request, *args, **kwargs):
        Permission.check_permissions(request.user, [permission_permission_grant, permission_permission_revoke])
        self.role = get_object_or_404(Role, pk=self.kwargs['pk'])
        self.left_list_title = _('Available permissions')
        self.right_list_title = _('Granted permissions')

        return super(SetupRolePermissionsView, self).dispatch(request, *args, **kwargs)

    def left_list(self):
        results = []
        for namespace, permissions in itertools.groupby(StoredPermission.objects.exclude(id__in=self.role.permissions.values_list('pk', flat=True)), lambda entry: entry.namespace):
            permission_options = [(unicode(permission.pk), permission) for permission in permissions]
            results.append((PermissionNamespace.get(namespace), permission_options))

        return results

    def right_list(self):
        results = []
        for namespace, permissions in itertools.groupby(self.role.permissions.all(), lambda entry: entry.namespace):
            permission_options = [(unicode(permission.pk), permission) for permission in permissions]
            results.append((PermissionNamespace.get(namespace), permission_options))

        return results

    def remove(self, item):
        permission = get_object_or_404(StoredPermission, pk=item)
        self.role.permissions.remove(permission)

    def get_context_data(self, **kwargs):
        data = super(SetupRolePermissionsView, self).get_context_data(**kwargs)
        data.update({
            'object': self.role,
            'title': _('Permissions for role: %s') % self.role,
        })

        return data


def role_list(request):
    Permission.check_permissions(request.user, [permission_role_view])

    context = {
        'object_list': Role.objects.all(),
        'title': _('Roles'),
        'hide_link': True,
    }

    return render_to_response('appearance/generic_list.html', context,
                              context_instance=RequestContext(request))


def role_permissions(request, role_id):
    Permission.check_permissions(request.user, [permission_permission_grant, permission_permission_revoke])

    role = get_object_or_404(Role, pk=role_id)

    return render_to_response('appearance/generic_list.html', {
        'object': role,
        'multi_select_item_properties': {
            'permission_id': lambda x: x.pk,
            'requester_id': lambda x: role.pk,
            'requester_app_label': lambda x: ContentType.objects.get_for_model(role).app_label,
            'requester_model': lambda x: ContentType.objects.get_for_model(role).model,
        },
        'title': _('Permissions for: %s') % role,
        'object_list': Permission.all(),
        'extra_columns': [
            {'name': _('Namespace'), 'attribute': encapsulate(lambda x: x.namespace)},
            {'name': _('Name'), 'attribute': encapsulate(lambda x: x.label)},
            {
                'name': _('Has permission'),
                'attribute': encapsulate(lambda x: two_state_template(x.requester_has_this(role))),
            },
        ],
        'hide_link': True,
        'hide_object': True,
    }, context_instance=RequestContext(request))
