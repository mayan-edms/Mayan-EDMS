from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation import Link

from .permissions import (PERMISSION_COMMENT_CREATE,
    PERMISSION_COMMENT_DELETE, PERMISSION_COMMENT_VIEW)
from .icons import (icon_comments_for_document, icon_comment_add, icon_comment_delete)

comment_delete = Link(text=_('delete'), view='comment_delete', args='object.pk', icon=icon_comment_delete, permissions=[PERMISSION_COMMENT_DELETE])
comment_multiple_delete = Link(text=_('delete'), view='comment_multiple_delete', args='object.pk', icon=icon_comment_delete, permissions=[PERMISSION_COMMENT_DELETE])
comment_add = Link(text=_('add comment'), view='comment_add', args='object.pk', icon=icon_comment_add, permissions=[PERMISSION_COMMENT_CREATE])
comments_for_document = Link(text=_('comments'), view='comments_for_document', args='object.pk', icon=icon_comments_for_document, permissions=[PERMISSION_COMMENT_VIEW], children_view_regex=['comment'])
