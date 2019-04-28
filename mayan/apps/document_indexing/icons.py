from __future__ import absolute_import, unicode_literals

from mayan.apps.appearance.classes import Icon
from mayan.apps.documents.icons import icon_document_type

icon_document_index_instance_list = Icon(
    driver_name='fontawesome', symbol='list-ul'
)
icon_index = Icon(driver_name='fontawesome', symbol='list-ul')
icon_document_type_index_templates = icon_index
icon_index_level_up = Icon(
    driver_name='fontawesomecss', css_classes='fa-level-up-alt fa-rotate-90'
)

icon_index_instance_node_with_documents = Icon(
    driver_name='fontawesome', symbol='folder'
)
icon_index_instances_rebuild = Icon(
    driver_name='fontawesome', symbol='list-ul'
)

icon_index_template_create = Icon(
    driver_name='fontawesome-dual', primary_symbol='list-ul',
    secondary_symbol='plus'
)
icon_index_template_delete = Icon(driver_name='fontawesome', symbol='times')
icon_index_template_document_types = icon_document_type
icon_index_template_edit = Icon(driver_name='fontawesome', symbol='pencil-alt')
icon_index_template_list = Icon(driver_name='fontawesome', symbol='list-ul')

icon_index_template_node_create = Icon(
    driver_name='fontawesome', symbol='plus'
)


icon_index_template_node_delete = Icon(
    driver_name='fontawesome', symbol='times'
)
icon_index_template_node_edit = Icon(
    driver_name='fontawesome', symbol='pencil-alt'
)

icon_index_template_node_tree_view = Icon(
    driver_name='fontawesome', symbol='folder-open'
)
