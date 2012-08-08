from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _
from django.db import transaction, DatabaseError

from documents.models import Document
from folders.models import Folder
from navigation.api import bind_links
from project_tools.api import register_tool
from taggit.models import Tag

from .api import make_trashable
from .links import trash_can_list, trash_can_items, trash_can_item_restore, trash_can_item_delete
from .models import TrashCan, TrashCanItem

register_tool(trash_can_list)
bind_links(['trash_can_list', TrashCan], trash_can_list, menu_name='secondary_menu')
bind_links([TrashCan], trash_can_items)
bind_links([TrashCanItem], [trash_can_item_restore, trash_can_item_delete])

@transaction.commit_on_success
def create_trash_cans():
    try:
        documents_trash_can, created = TrashCan.objects.get_or_create(name='documents', defaults={'label': _(u'Documents')})
        folders_trash_can, created = TrashCan.objects.get_or_create(name='folders', defaults={'label': _(u'Folders')})
        tags_trash_can, created = TrashCan.objects.get_or_create(name='tags', defaults={'label': _(u'Tags')})
    except DatabaseError:
        transaction.rollback()
    else:
        make_trashable(Document, documents_trash_can)
        make_trashable(Folder, folders_trash_can)
        make_trashable(Tag, tags_trash_can)

create_trash_cans()
