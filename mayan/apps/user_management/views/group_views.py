from django.contrib.auth.models import Group
from django.template import RequestContext
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from mayan.apps.views.generics import (
    AddRemoveView, MultipleObjectDeleteView, SingleObjectCreateView,
    SingleObjectDetailView, SingleObjectEditView, SingleObjectListView
)

from ..icons import icon_group_setup
from ..links import link_group_create
from ..permissions import (
    permission_group_create, permission_group_delete, permission_group_edit,
    permission_group_view, permission_user_edit
)
from ..querysets import get_user_queryset


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

    def get_secondary_object_source_queryset(self):
        return get_user_queryset(user=self.request.user)
