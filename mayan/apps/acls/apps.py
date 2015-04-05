from __future__ import unicode_literals

from django import apps
from django.db.models.signals import post_migrate
from django.utils.translation import ugettext_lazy as _

from common.menus import (
    menu_multi_item, menu_object, menu_secondary, menu_setup, menu_sidebar
)

from .classes import (
    AccessHolder, AccessObject, AccessObjectClass, ClassAccessHolder
)
from .links import (
    link_acl_class_acl_detail, link_acl_class_acl_list, link_acl_class_grant,
    link_acl_class_list, link_acl_class_new_holder_for, link_acl_class_revoke,
    link_acl_detail, link_acl_grant, link_acl_holder_new, link_acl_revoke,
    link_acl_setup_valid_classes
)
from .models import CreatorSingleton


def create_creator_user(sender, **kwargs):
    if kwargs['app_config'].__class__ == ACLsApp:
        CreatorSingleton.objects.get_or_create()


class ACLsApp(apps.AppConfig):
    name = 'acls'
    verbose_name = _('ACLs')

    def ready(self):
        menu_multi_item.bind_links(links=[link_acl_class_grant, link_acl_class_revoke], sources=['acls:acl_class_acl_detail'])
        menu_multi_item.bind_links(links=[link_acl_grant, link_acl_revoke], sources=['acls:acl_detail'])
        menu_object.bind_links(links=[link_acl_class_acl_detail], sources=[ClassAccessHolder])
        menu_object.bind_links(links=[link_acl_class_acl_list, link_acl_class_new_holder_for], sources=[AccessObjectClass])
        menu_object.bind_links(links=[link_acl_detail], sources=[AccessHolder])
        menu_secondary.bind_links(
            links=[link_acl_class_list],
            sources=[
                'acls:acl_setup_valid_classes', 'acls:acl_class_acl_list',
                'acls:acl_class_new_holder_for', 'acls:acl_class_acl_detail',
                'acls:acl_class_multiple_grant',
                'acls:acl_class_multiple_revoke'
            ],
         )
        menu_setup.bind_links(links=[link_acl_setup_valid_classes])
        menu_sidebar.bind_links(links=[link_acl_holder_new], sources=[AccessObject])

        post_migrate.connect(create_creator_user, dispatch_uid='create_creator_user')
