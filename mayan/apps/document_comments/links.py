from __future__ import unicode_literals, absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation import Link

from .permissions import (
    PERMISSION_COMMENT_CREATE, PERMISSION_COMMENT_DELETE,
    PERMISSION_COMMENT_VIEW
)

link_comment_add = Link(permissions=[PERMISSION_COMMENT_CREATE], text=_('Add comment'), view='comments:comment_add', args='object.pk')
link_comment_delete = Link(permissions=[PERMISSION_COMMENT_DELETE], text=_('Delete'), view='comments:comment_delete', args='object.pk')
link_comment_multiple_delete = Link(permissions=[PERMISSION_COMMENT_DELETE], text=_('Delete'), view='comments:comment_multiple_delete', args='object.pk')
link_comments_for_document = Link(permissions=[PERMISSION_COMMENT_VIEW], text=_('Comments'), view='comments:comments_for_document', args='object.pk')
