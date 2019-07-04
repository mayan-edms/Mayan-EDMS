from __future__ import unicode_literals

from django.apps import apps
from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.db.models.signals import post_save
from django.utils import six
from django.utils.translation import ugettext_lazy as _

from mayan.apps.acls.classes import ModelPermission
from mayan.apps.acls.links import link_acl_list
from mayan.apps.acls.permissions import permission_acl_edit, permission_acl_view
from mayan.apps.common.apps import MayanAppConfig
from mayan.apps.common.html_widgets import TwoStateWidget
from mayan.apps.common.menus import (
    menu_list_facet, menu_multi_item, menu_object, menu_secondary, menu_setup,
    menu_user
)
from mayan.apps.dashboards.dashboards import dashboard_main
from mayan.apps.events.classes import ModelEventType
from mayan.apps.events.links import (
    link_events_for_object, link_object_event_types_user_subcriptions_list
)
from mayan.apps.events.permissions import permission_events_view
from mayan.apps.metadata.classes import MetadataLookup
from mayan.apps.navigation.classes import SourceColumn
from mayan.apps.rest_api.fields import DynamicSerializerField

from .dashboard_widgets import (
    DashboardWidgetGroupTotal, DashboardWidgetUserTotal
)
from .events import (
    event_group_created, event_group_edited, event_user_created,
    event_user_edited
)
from .handlers import (
    handler_initialize_new_user_options, handler_user_logged_in,
    handler_user_logged_out
)
from .links import (
    link_current_user_details, link_current_user_edit, link_group_create,
    link_group_delete, link_group_edit, link_group_list, link_group_user_list,
    link_group_setup, link_user_create, link_user_delete, link_user_edit,
    link_user_group_list, link_user_list, link_user_multiple_delete,
    link_user_set_options, link_user_setup, separator_user_label,
    text_user_label
)
from .methods import (
    get_method_group_save, get_method_user_save, method_user_get_absolute_url,
    method_group_get_users, method_group_users_add, method_group_users_remove,
    method_user_get_groups, method_user_groups_add, method_user_groups_remove
)

from .permissions import (
    permission_group_delete, permission_group_edit,
    permission_group_view, permission_user_delete, permission_user_edit,
    permission_user_view
)
from .search import *  # NOQA


def get_groups():
    Group = apps.get_model(app_label='auth', model_name='Group')
    return ','.join([group.name for group in Group.objects.all()])


def get_users():
    return ','.join(
        [
            user.get_full_name() or user.username
            for user in get_user_model().objects.all()
        ]
    )


class UserManagementApp(MayanAppConfig):
    app_namespace = 'user_management'
    app_url = 'accounts'
    has_rest_api = True
    has_tests = True
    name = 'mayan.apps.user_management'
    verbose_name = _('User management')

    def ready(self):
        super(UserManagementApp, self).ready()
        from actstream import registry

        Group = apps.get_model(app_label='auth', model_name='Group')
        User = get_user_model()

        DynamicSerializerField.add_serializer(
            klass=get_user_model(),
            serializer_class='mayan.apps.user_management.serializers.UserSerializer'
        )

        # Silence UnorderedObjectListWarning
        # "Pagination may yield inconsistent result"
        # TODO: Remove on Django 2.x
        Group._meta.ordering = ('name',)
        Group._meta.verbose_name = _('Group')
        Group._meta.verbose_name_plural = _('Groups')
        Group._meta.get_field('name').verbose_name = _('Name')

        # Silence UnorderedObjectListWarning
        # "Pagination may yield inconsistent result"
        # TODO: Remove on Django 2.x
        User._meta.ordering = ('pk',)
        User._meta.verbose_name = _('User')
        User._meta.verbose_name_plural = _('Users')
        User._meta.ordering = ('last_name', 'first_name')

        User._meta.get_field('username').verbose_name = _('Username')
        User._meta.get_field('first_name').verbose_name = _('First name')
        User._meta.get_field('last_name').verbose_name = _('Last name')
        User._meta.get_field('email').verbose_name = _('Email')
        User._meta.get_field('is_active').verbose_name = _('Is active?')
        if six.PY3:
            User.has_usable_password.short_description = _(
                'Has usable password?'
            )
        else:
            User.has_usable_password.__func__.short_description = _(
                'Has usable password?'
            )

        Group.add_to_class(
            name='get_users', value=method_group_get_users
        )
        Group.add_to_class(
            name='users_add', value=method_group_users_add
        )
        Group.add_to_class(
            name='users_remove', value=method_group_users_remove
        )
        Group.add_to_class(name='save', value=get_method_group_save())

        MetadataLookup(
            description=_('All the groups.'), name='groups',
            value=get_groups
        )
        MetadataLookup(
            description=_('All the users.'), name='users',
            value=get_users
        )

        ModelEventType.register(
            event_types=(event_group_created, event_group_edited), model=Group
        )

        ModelEventType.register(
            event_types=(event_user_created, event_user_edited), model=User
        )

        ModelPermission.register(
            model=Group, permissions=(
                permission_acl_edit, permission_acl_view,
                permission_events_view, permission_group_delete,
                permission_group_edit, permission_group_view,
            )
        )
        ModelPermission.register(
            model=User, permissions=(
                permission_acl_edit, permission_acl_view,
                permission_events_view, permission_user_delete,
                permission_user_edit, permission_user_view
            )
        )

        SourceColumn(
            attribute='name', is_identifier=True, is_sortable=True,
            source=Group
        )
        SourceColumn(
            attribute='user_set.count', label=_('Users'), source=Group
        )

        SourceColumn(
            attribute='username', is_object_absolute_url=True,
            is_identifier=True, is_sortable=True, source=User
        )
        SourceColumn(
            attribute='first_name', is_sortable=True, source=User
        )
        SourceColumn(
            attribute='last_name', is_sortable=True, source=User
        )
        SourceColumn(
            attribute='email', is_sortable=True, source=User
        )
        SourceColumn(
            attribute='is_active', is_sortable=True, source=User,
            widget=TwoStateWidget
        )
        SourceColumn(
            attribute='has_usable_password', source=User,
            widget=TwoStateWidget
        )

        User.add_to_class(
            name='get_absolute_url', value=method_user_get_absolute_url
        )
        User.add_to_class(
            name='get_groups', value=method_user_get_groups
        )
        User.add_to_class(
            name='groups_add', value=method_user_groups_add
        )
        User.add_to_class(
            name='groups_remove', value=method_user_groups_remove
        )
        User.add_to_class(name='save', value=get_method_user_save())

        dashboard_main.add_widget(
            widget=DashboardWidgetUserTotal, order=99
        )
        dashboard_main.add_widget(
            widget=DashboardWidgetGroupTotal, order=99
        )

        menu_list_facet.bind_links(
            links=(
                link_acl_list, link_events_for_object,
                link_object_event_types_user_subcriptions_list,
                link_group_user_list,
            ), sources=(Group,)
        )
        menu_list_facet.bind_links(
            links=(
                link_acl_list, link_events_for_object,
                link_object_event_types_user_subcriptions_list,
                link_user_group_list, link_user_set_options
            ), sources=(User,)
        )
        menu_multi_item.bind_links(
            links=(link_user_multiple_delete,),
            sources=('user_management:user_list',)
        )
        menu_object.bind_links(
            links=(link_group_edit,),
            sources=(Group,)
        )
        menu_object.bind_links(
            links=(link_group_delete,), position=99,
            sources=(Group,)
        )
        menu_object.bind_links(
            links=(link_user_delete, link_user_edit,), sources=(User,)
        )
        menu_secondary.bind_links(
            links=(link_group_list, link_group_create), sources=(
                'user_management:group_multiple_delete',
                'user_management:group_list', 'user_management:group_create',
                Group
            )
        )
        menu_secondary.bind_links(
            links=(link_user_list, link_user_create), sources=(
                User, 'authentication:user_multiple_set_password',
                'user_management:user_multiple_delete',
                'user_management:user_list', 'user_management:user_create'
            )
        )
        menu_setup.bind_links(links=(link_user_setup, link_group_setup))
        menu_user.bind_links(
            links=(
                text_user_label, separator_user_label,
                link_current_user_details, link_current_user_edit,
            ), position=0
        )

        post_save.connect(
            dispatch_uid='user_management_handler_initialize_new_user_options',
            receiver=handler_initialize_new_user_options,
            sender=User
        )

        user_logged_in.connect(
            dispatch_uid='user_management_handler_user_logged_in',
            receiver=handler_user_logged_in,
            sender=User
        )
        user_logged_out.connect(
            dispatch_uid='user_management_handler_user_logged_out',
            receiver=handler_user_logged_out,
            sender=User
        )

        registry.register(Group)
        registry.register(User)
