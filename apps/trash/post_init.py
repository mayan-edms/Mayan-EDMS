from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation.api import bind_links

from .links import trash_can_list, trash_can_items, trash_can_item_restore, trash_can_item_delete
from .models import TrashCan, TrashCanItem


def create_trash_cans():
    model_set = [('documents.Document', _(u'Documents')), ('folders.Folder', _(u'Folders')), ('taggit.Tag', _(u'Tags'))]
    for model_info in model_set:
        TrashCan.objects.make_trashable(*model_info)


bind_links(['trash_can_list', TrashCan], trash_can_list, menu_name='secondary_menu')
bind_links([TrashCan], trash_can_items)
bind_links([TrashCanItem], [trash_can_item_restore, trash_can_item_delete])
create_trash_cans()
