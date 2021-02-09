from django.utils.translation import ugettext_lazy as _

from mayan.apps.navigation.classes import Link

from .icons import (
    icon_comment_add, icon_comment_delete, icon_comment_edit,
    icon_comments_for_document
)
from .permissions import (
    permission_document_comment_create, permission_document_comment_delete,
    permission_document_comment_edit, permission_document_comment_view
)

link_comment_add = Link(
    args='object.pk', icon=icon_comment_add,
    permissions=(permission_document_comment_create,), text=_('Add comment'),
    view='comments:comment_add',
)
link_comment_delete = Link(
    args='object.pk', icon=icon_comment_delete,
    permissions=(permission_document_comment_delete,), tags='dangerous',
    text=_('Delete'), view='comments:comment_delete',
)
link_comment_edit = Link(
    args='object.pk', icon=icon_comment_edit,
    permissions=(permission_document_comment_edit,),
    text=_('Edit'), view='comments:comment_edit',
)
link_comments_for_document = Link(
    args='resolved_object.pk', icon=icon_comments_for_document,
    permissions=(permission_document_comment_view,), text=_('Comments'),
    view='comments:comments_for_document',
)
