from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation import Link

from .icons import (icon_trash_cans, icon_trash_can_items, icon_trash_can_item_restore,
    icon_trash_can_item_delete)

trash_can_list = Link(text=_(u'trash bins'), view='trash_can_list', icon=icon_trash_cans)
trash_can_items = Link(text=_(u'items'), view='trash_can_items', args='trash_can.pk', icon=icon_trash_can_items)
trash_can_item_restore = Link(text=_(u'restore'), view='trash_can_item_restore', args='trash_can_item.pk', icon=icon_trash_can_item_restore)
trash_can_item_delete = Link(text=_(u'delete'), view='trash_can_item_delete', args='trash_can_item.pk', icon=icon_trash_can_item_delete)
