from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _
from django.db import transaction, DatabaseError

from documents.models import Document
from navigation.api import bind_links
from project_tools.api import register_tool

from .api import make_trashable
from .links import trash_can_list, trash_can_items, trash_can_item_restore
from .models import TrashCan, TrashCanItem

register_tool(trash_can_list)
bind_links(['trash_can_list', TrashCan, TrashCanItem], trash_can_list, menu_name='secondary_menu')
bind_links([TrashCan], trash_can_items)
bind_links([TrashCanItem], trash_can_item_restore)

@transaction.commit_on_success
def create_trash_cans():
    try:
        documents_trash_can, created = TrashCan.objects.get_or_create(name='documents', defaults={'label': _(u'documents')})
    except DatabaseError:
        transaction.rollback()
    else:
        make_trashable(Document, documents_trash_can)

create_trash_cans()
