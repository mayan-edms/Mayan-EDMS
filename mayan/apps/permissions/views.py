from django.contrib.auth.models import Group
from django.template import RequestContext
from django.urls import reverse_lazy
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _

from mayan.apps.user_management.permissions import permission_group_edit
from mayan.apps.views.generics import (
    AddRemoveView, SingleObjectCreateView, SingleObjectDeleteView,
    SingleObjectEditView, SingleObjectListView
)

from .icons import icon_role_list
from .links import link_role_create
from .models import Role, StoredPermission
from .permissions import (
    permission_role_view, permission_role_create, permission_role_delete,
    permission_role_edit
)


class GroupRolesView(AddRemoveView):
    main_object_method_add_name = 'roles_add'
    main_object_method_remove_name = 'roles_remove'
    main_object_model = Group
    main_object_permission = permission_group_edit
    main_object_pk_url_kwarg = 'group_id'
    secondary_object_model = Role
    secondary_object_permission = permission_role_edit
    list_available_title = _('Available roles')
    list_added_title = _('Group roles')
    related_field = 'roles'

    def get_actions_extra_kwargs(self):
        return {'_event_actor': self.request.user}

    def get_extra_context(self):
        return {
            'object': self.main_object,
            'title': _('Roles of group: %s') % self.main_object,
        }


class RoleCreateView(SingleObjectCreateView):
    fields = ('label',)
    model = Role
    view_permission = permission_role_create
    post_action_redirect = reverse_lazy(viewname='permissions:role_list')

    def get_extra_context(self):
        return {'title': _('Create new role')}

    def get_instance_extra_data(self):
        return {'_event_actor': self.request.user}


class RoleDeleteView(SingleObjectDeleteView):
    model = Role
    object_permission = permission_role_delete
    pk_url_kwarg = 'role_id'
    post_action_redirect = reverse_lazy(viewname='permissions:role_list')


class RoleEditView(SingleObjectEditView):
    fields = ('label',)
    model = Role
    object_permission = permission_role_edit
    pk_url_kwarg = 'role_id'

    def get_instance_extra_data(self):
        return {'_event_actor': self.request.user}


class SetupRoleMembersView(AddRemoveView):
    main_object_method_add_name = 'groups_add'
    main_object_method_remove_name = 'groups_remove'
    main_object_model = Role
    main_object_permission = permission_role_edit
    main_object_pk_url_kwarg = 'role_id'
    secondary_object_model = Group
    secondary_object_permission = permission_group_edit
    list_available_title = _('Available groups')
    list_added_title = _('Role groups')
    related_field = 'groups'

    def get_actions_extra_kwargs(self):
        return {'_event_actor': self.request.user}

    def get_extra_context(self):
        return {
            'object': self.main_object,
            'title': _('Groups of role: %s') % self.main_object,
            'subtitle': _(
                'Add groups to be part of a role. They will '
                'inherit the role\'s permissions and access controls.'
            ),
        }


class SetupRolePermissionsView(AddRemoveView):
    grouped = True
    main_object_method_add_name = 'permissions_add'
    main_object_method_remove_name = 'permissions_remove'
    main_object_model = Role
    main_object_permission = permission_role_edit
    main_object_pk_url_kwarg = 'role_id'
    list_available_title = _('Available permissions')
    list_added_title = _('Granted permissions')
    related_field = 'permissions'
    secondary_object_model = StoredPermission

    def generate_choices(self, queryset):
        namespaces_dictionary = {}

        # Sort permissions by their translatable label
        object_list = sorted(
            queryset,
            key=lambda permission: permission.volatile_permission.label
        )

        # Group permissions by namespace
        for permission in object_list:
            namespaces_dictionary.setdefault(
                permission.volatile_permission.namespace.label,
                []
            )
            namespaces_dictionary[
                permission.volatile_permission.namespace.label
            ].append(
                (permission.pk, force_text(s=permission))
            )

        # Sort permissions by their translatable namespace label
        return sorted(namespaces_dictionary.items())

    def get_actions_extra_kwargs(self):
        return {'_event_actor': self.request.user}

    def get_extra_context(self):
        return {
            'object': self.main_object,
            'subtitle': _(
                'Permissions granted here will apply to the entire system '
                'and all objects.'
            ),
            'title': _('Permissions for role: %s') % self.main_object,
        }


class RoleListView(SingleObjectListView):
    model = Role
    object_permission = permission_role_view

    def get_extra_context(self):
        return {
            'hide_link': True,
            'hide_object': True,
            'no_results_icon': icon_role_list,
            'no_results_main_link': link_role_create.resolve(
                context=RequestContext(request=self.request)
            ),
            'no_results_text': _(
                'Roles are authorization units. They contain '
                'user groups which inherit the role permissions for the '
                'entire system. Roles can also part of access '
                'controls lists. Access controls list are permissions '
                'granted to a role for specific objects which its group '
                'members inherit.'
            ),
            'no_results_title': _('There are no roles'),
            'title': _('Roles'),
        }
