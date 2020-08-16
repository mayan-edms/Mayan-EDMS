from django.utils.translation import ugettext_lazy as _

from mayan.apps.documents.permissions import permission_document_type_edit
from mayan.apps.navigation.classes import Link

from .permissions import (
    permission_web_link_create, permission_web_link_delete,
    permission_web_link_edit, permission_web_link_instance_view,
)

link_document_type_web_links = Link(
    args='resolved_object.pk',
    icon_class_path='mayan.apps.web_links.icons.icon_document_type_web_links',
    permissions=(permission_document_type_edit,), text=_('Web links'),
    view='web_links:document_type_web_links',
)
link_document_web_link_list = Link(
    args='resolved_object.pk',
    icon_class_path='mayan.apps.web_links.icons.icon_document_web_link_list',
    permissions=(permission_web_link_instance_view,), text=_('Web links'),
    view='web_links:document_web_link_list',
)
link_web_link_create = Link(
    icon_class_path='mayan.apps.web_links.icons.icon_web_link_create',
    permissions=(permission_web_link_create,),
    text=_('Create new web link'), view='web_links:web_link_create'
)
link_web_link_delete = Link(
    args='object.pk',
    icon_class_path='mayan.apps.web_links.icons.icon_web_link_delete',
    permissions=(permission_web_link_delete,),
    tags='dangerous', text=_('Delete'), view='web_links:web_link_delete',
)
link_web_link_document_types = Link(
    args='object.pk',
    icon_class_path='mayan.apps.web_links.icons.icon_web_link_document_types',
    permissions=(permission_web_link_edit,),
    text=_('Document types'), view='web_links:web_link_document_types',
)
link_web_link_edit = Link(
    args='object.pk',
    icon_class_path='mayan.apps.web_links.icons.icon_web_link_edit',
    permissions=(permission_web_link_edit,),
    text=_('Edit'), view='web_links:web_link_edit',
)
link_web_link_instance_view = Link(
    icon_class_path='mayan.apps.web_links.icons.icon_web_link_instance_view',
    args=('document.pk', 'object.pk',),
    permissions=(permission_web_link_instance_view,), tags='new_window',
    text=_('Navigate'), view='web_links:web_link_instance_view',
)
link_web_link_list = Link(
    icon_class_path='mayan.apps.web_links.icons.icon_web_link_list',
    text=_('Web links'), view='web_links:web_link_list'
)
link_web_link_setup = Link(
    icon_class_path='mayan.apps.web_links.icons.icon_web_link_setup',
    permissions=(permission_web_link_create,), text=_('Web links'),
    view='web_links:web_link_list'
)
