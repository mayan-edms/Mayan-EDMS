from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from mayan.apps.navigation.classes import Link
from mayan.apps.navigation.utils import get_cascade_condition

from .permissions import (
    permission_tag_attach, permission_tag_create, permission_tag_delete,
    permission_tag_edit, permission_tag_remove, permission_tag_view
)


link_document_multiple_tag_multiple_remove = Link(
    icon_class_path='mayan.apps.tags.icons.icon_document_tag_multiple_remove',
    text=_('Remove tag'), view='tags:multiple_documents_selection_tag_remove'
)
link_document_multiple_attach_multiple_tag = Link(
    icon_class_path='mayan.apps.tags.icons.icon_document_tag_multiple_attach',
    text=_('Attach tags'), view='tags:multiple_documents_tag_attach'
)
link_document_tag_list = Link(
    args='resolved_object.pk',
    icon_class_path='mayan.apps.tags.icons.icon_document_tag_list',
    permissions=(permission_tag_view,), text=_('Tags'),
    view='tags:document_tag_list'
)
link_document_tag_multiple_remove = Link(
    args='object.id',
    icon_class_path='mayan.apps.tags.icons.icon_document_tag_multiple_remove',
    permissions=(permission_tag_remove,), text=_('Remove tags'),
    view='tags:single_document_multiple_tag_remove'
)
link_document_tag_multiple_attach = Link(
    args='object.pk',
    icon_class_path='mayan.apps.tags.icons.icon_document_tag_multiple_attach',
    permissions=(permission_tag_attach,), text=_('Attach tags'),
    view='tags:tag_attach'
)

link_tag_create = Link(
    icon_class_path='mayan.apps.tags.icons.icon_tag_create',
    permissions=(permission_tag_create,),
    text=_('Create new tag'), view='tags:tag_create'
)
link_tag_delete = Link(
    args='object.id',
    icon_class_path='mayan.apps.tags.icons.icon_tag_delete',
    permissions=(permission_tag_delete,), tags='dangerous',
    text=_('Delete'), view='tags:tag_delete'
)
link_tag_edit = Link(
    args='object.id',
    icon_class_path='mayan.apps.tags.icons.icon_tag_edit',
    permissions=(permission_tag_edit,), text=_('Edit'),
    view='tags:tag_edit'
)
link_tag_list = Link(
    condition=get_cascade_condition(
        app_label='tags', model_name='Tag',
        object_permission=permission_tag_view,
    ), icon_class_path='mayan.apps.tags.icons.icon_tag_list',
    text=_('All'), view='tags:tag_list'
)
link_tag_multiple_delete = Link(
    icon_class_path='mayan.apps.tags.icons.icon_tag_delete',
    permissions=(permission_tag_delete,), text=_('Delete'),
    view='tags:tag_multiple_delete'
)
link_tag_document_list = Link(
    args='object.id',
    icon_class_path='mayan.apps.tags.icons.icon_tag_document_list',
    text=('Documents'), view='tags:tag_document_list'
)
