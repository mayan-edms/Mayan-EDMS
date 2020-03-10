from __future__ import unicode_literals

from django.apps import apps
from django.utils.translation import ugettext_lazy as _

from mayan.apps.navigation.classes import Link

from .icons import (
    icon_acl_delete, icon_acl_list, icon_acl_new, icon_acl_permissions
)
from .permissions import permission_acl_view, permission_acl_edit


def get_kwargs_factory(variable_name):
    def get_kwargs(context):
        ContentType = apps.get_model(
            app_label='contenttypes', model_name='ContentType'
        )

        content_type = ContentType.objects.get_for_model(
            context[variable_name]
        )
        return {
            'app_label': '"{}"'.format(content_type.app_label),
            'model_name': '"{}"'.format(content_type.model),
            'object_id': '{}.pk'.format(variable_name)
        }

    return get_kwargs


link_acl_create = Link(
    icon_class=icon_acl_new, kwargs=get_kwargs_factory('resolved_object'),
    permissions=(permission_acl_edit,), text=_('New ACL'),
    view='acls:acl_create'
)
link_acl_delete = Link(
    args='resolved_object.pk', icon_class=icon_acl_delete,
    permissions=(permission_acl_edit,), tags='dangerous', text=_('Delete'),
    view='acls:acl_delete'
)
link_acl_list = Link(
    icon_class=icon_acl_list, kwargs=get_kwargs_factory('resolved_object'),
    permissions=(permission_acl_view,), text=_('ACLs'), view='acls:acl_list'
)
link_acl_permissions = Link(
    args='resolved_object.pk', icon_class=icon_acl_permissions,
    permissions=(permission_acl_edit,),
    text=_('Permissions'), view='acls:acl_permissions'
)
