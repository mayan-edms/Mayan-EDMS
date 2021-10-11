from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.urls import reverse, reverse_lazy
from django.utils.translation import ugettext_lazy as _

from mayan.apps.views.generics import (
    AddRemoveView, MultipleObjectDeleteView, SingleObjectCreateView,
    SingleObjectDetailView, SingleObjectEditView, SingleObjectListView
)
from mayan.apps.views.mixins import ExternalObjectViewMixin

from .forms import UserForm
from .icons import icon_group_setup, icon_user_setup
from .links import link_group_create, link_user_create
from .permissions import (
    permission_group_create, permission_group_delete, permission_group_edit,
    permission_group_view, permission_user_create, permission_user_delete,
    permission_user_edit, permission_user_view
)
from .querysets import get_user_queryset


class CurrentUserDetailView(SingleObjectDetailView):
    fields = (
        'username', 'first_name', 'last_name', 'email', 'last_login',
        'date_joined', 'groups'
    )

    def get_extra_context(self, **kwargs):
        return {
            'object': None,
            'title': _('Current user details'),
        }

    def get_object(self):
        return self.request.user


class CurrentUserEditView(SingleObjectEditView):
    extra_context = {'object': None, 'title': _('Edit current user details')}
    form_class = UserForm
    post_action_redirect = reverse_lazy(
        viewname='user_management:current_user_details'
    )

    def get_object(self):
        return self.request.user


class GroupCreateView(SingleObjectCreateView):
    extra_context = {'title': _('Create new group')}
    fields = ('name',)
    model = Group
    post_action_redirect = reverse_lazy(
        viewname='user_management:group_list'
    )
    view_permission = permission_group_create

    def get_instance_extra_data(self):
        return {'_event_actor': self.request.user}


class GroupDeleteView(MultipleObjectDeleteView):
    error_message = _('Error deleting group "%(instance)s"; %(exception)s')
    model = Group
    object_permission = permission_group_delete
    pk_url_kwarg = 'group_id'
    post_action_redirect = reverse_lazy(
        viewname='user_management:group_list'
    )
    success_message_single = _('Group "%(object)s" deleted successfully.')
    success_message_singular = _('%(count)d group deleted successfully.')
    success_message_plural = _('%(count)d groups deleted successfully.')
    title_single = _('Delete group: %(object)s.')
    title_singular = _('Delete the %(count)d selected group.')
    title_plural = _('Delete the %(count)d selected groups.')


class GroupDetailView(SingleObjectDetailView):
    fields = ('name',)
    model = Group
    object_permission = permission_group_view
    pk_url_kwarg = 'group_id'

    def get_extra_context(self, **kwargs):
        return {
            'object': self.object,
            'title': _('Details of group: %s') % self.object
        }


class GroupEditView(SingleObjectEditView):
    fields = ('name',)
    model = Group
    object_permission = permission_group_edit
    pk_url_kwarg = 'group_id'
    post_action_redirect = reverse_lazy(
        viewname='user_management:group_list'
    )

    def get_extra_context(self):
        return {
            'object': self.object,
            'title': _('Edit group: %s') % self.object,
        }

    def get_instance_extra_data(self):
        return {'_event_actor': self.request.user}


class GroupListView(SingleObjectListView):
    model = Group
    object_permission = permission_group_view

    def get_extra_context(self):
        return {
            'hide_link': True,
            'hide_object': True,
            'no_results_icon': icon_group_setup,
            'no_results_main_link': link_group_create.resolve(
                context=RequestContext(request=self.request)
            ),
            'no_results_text': _(
                'User groups are organizational units. They should '
                'mirror the organizational units of your organization. '
                'Groups can\'t be used for access control. Use roles '
                'for permissions and access control, add groups to '
                'them.'
            ),
            'no_results_title': _('There are no user groups'),
            'title': _('Groups'),
        }


class GroupUsersView(AddRemoveView):
    main_object_method_add_name = 'users_add'
    main_object_method_remove_name = 'users_remove'
    main_object_model = Group
    main_object_permission = permission_group_edit
    main_object_pk_url_kwarg = 'group_id'
    secondary_object_permission = permission_user_edit
    secondary_object_source_queryset = get_user_queryset()
    list_available_title = _('Available users')
    list_added_title = _('Group users')

    def get_actions_extra_kwargs(self):
        return {'_event_actor': self.request.user}

    def get_extra_context(self):
        return {
            'object': self.main_object,
            'title': _('Users of group: %s') % self.main_object,
        }

    def get_list_added_queryset(self):
        return self.main_object.get_users(
            permission=permission_user_edit, user=self.request.user
        )


class UserCreateView(SingleObjectCreateView):
    extra_context = {
        'title': _('Create new user'),
    }
    form_class = UserForm
    view_permission = permission_user_create

    def form_valid(self, form):
        super().form_valid(form=form)
        return HttpResponseRedirect(
            reverse(
                viewname='authentication:user_set_password', kwargs={
                    'user_id': self.object.pk
                }
            )
        )

    def get_instance_extra_data(self):
        return {'_event_actor': self.request.user}


class UserDeleteView(MultipleObjectDeleteView):
    error_message = _('Error deleting user "%(instance)s"; %(exception)s')
    object_permission = permission_user_delete
    pk_url_kwarg = 'user_id'
    post_action_redirect = reverse_lazy(viewname='user_management:user_list')
    source_queryset = get_user_queryset()
    success_message_single = _('User "%(object)s" deleted successfully.')
    success_message_singular = _('%(count)d user deleted successfully.')
    success_message_plural = _('%(count)d users deleted successfully.')
    title_single = _('Delete user: %(object)s.')
    title_singular = _('Delete the %(count)d selected user.')
    title_plural = _('Delete the %(count)d selected users.')


class UserDetailView(SingleObjectDetailView):
    fields = (
        'username', 'first_name', 'last_name', 'email', 'last_login',
        'date_joined', 'groups',
    )
    object_permission = permission_user_view
    pk_url_kwarg = 'user_id'
    source_queryset = get_user_queryset()

    def get_extra_context(self, **kwargs):
        return {
            'object': self.object,
            'title': _('Details of user: %s') % self.object
        }


class UserEditView(SingleObjectEditView):
    fields = ('username', 'first_name', 'last_name', 'email', 'is_active',)
    object_permission = permission_user_edit
    pk_url_kwarg = 'user_id'
    post_action_redirect = reverse_lazy(
        viewname='user_management:user_list'
    )
    source_queryset = get_user_queryset()

    def get_extra_context(self):
        return {
            'object': self.object,
            'title': _('Edit user: %s') % self.object,
        }

    def get_instance_extra_data(self):
        return {'_event_actor': self.request.user}


class UserGroupsView(AddRemoveView):
    main_object_method_add_name = 'groups_add'
    main_object_method_remove_name = 'groups_remove'
    main_object_permission = permission_user_edit
    main_object_source_queryset = get_user_queryset()
    main_object_pk_url_kwarg = 'user_id'
    secondary_object_model = Group
    secondary_object_permission = permission_group_edit
    list_available_title = _('Available groups')
    # Translators: "User groups" here refer to the group list of a specific
    # user.
    list_added_title = _('User groups')

    def get_actions_extra_kwargs(self):
        return {'_event_actor': self.request.user}

    def get_extra_context(self):
        return {
            'object': self.main_object,
            'title': _('Groups of user: %s') % self.main_object,
        }

    def get_list_added_queryset(self):
        return self.main_object.get_groups(
            permission=permission_group_edit, user=self.request.user
        )


class UserListView(SingleObjectListView):
    object_permission = permission_user_view
    source_queryset = get_user_queryset()

    def get_extra_context(self):
        return {
            'hide_link': True,
            'hide_object': True,
            'no_results_icon': icon_user_setup,
            'no_results_main_link': link_user_create.resolve(
                context=RequestContext(request=self.request)
            ),
            'no_results_text': _(
                'User accounts can be create from this view. After creating '
                'a user account you will prompted to set a password for it. '
            ),
            'no_results_title': _('There are no user accounts'),
            'title': _('Users'),
        }


class UserOptionsEditView(ExternalObjectViewMixin, SingleObjectEditView):
    external_object_permission = permission_user_edit
    external_object_pk_url_kwarg = 'user_id'
    external_object_queryset = get_user_queryset()
    fields = ('block_password_change',)

    def get_extra_context(self):
        return {
            'title': _(
                'Edit options for user: %s'
            ) % self.external_object,
            'object': self.external_object
        }

    def get_object(self):
        return self.external_object.user_options

    def get_post_action_redirect(self):
        return reverse(viewname='user_management:user_list')
