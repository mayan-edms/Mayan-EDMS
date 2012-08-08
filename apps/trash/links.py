from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation.api import Link


trash_can_list = Link(text=_(u'trash cans'), view='trash_can_list', sprite='bin_closed', icon='bin_closed.png')
trash_can_items = Link(text=_(u'items'), view='trash_can_items', args='trash_can.pk', sprite='bin')
trash_can_item_restore = Link(text=_(u'restore'), view='trash_can_item_restore', args='trash_can_item.pk', sprite='bin_empty')
trash_can_item_delete = Link(text=_(u'delete'), view='trash_can_item_delete', args='trash_can_item.pk', sprite='delete')
