from __future__ import absolute_import

from icons.literals import (FOLDER, FOLDER_PAGE, TAB, TAB_ADD, TAB_EDIT,
    TAB_DELETE, INDEX, NODE_TREE, NODE_TREE_ADD, NODE_TREE_EDIT,
    NODE_TREE_DELETE, ARROW_UP, LAYOUT, BULLET_GO)
from icons import Icon

icon_index_setup = Icon(TAB)
icon_index_setup_list = Icon(TAB)
icon_index_setup_create = Icon(TAB_ADD)
icon_index_setup_edit = Icon(TAB_EDIT)
icon_index_setup_delete = Icon(TAB_DELETE)
icon_index_setup_view = Icon(NODE_TREE)
icon_index_setup_document_types = Icon(LAYOUT)

icon_template_node_create = Icon(NODE_TREE_ADD)
icon_template_node_edit = Icon(NODE_TREE_EDIT)
icon_template_node_delete = Icon(NODE_TREE_DELETE)

icon_index_list = Icon(TAB)
icon_index_parent = Icon(ARROW_UP)
icon_document_index_list = Icon(FOLDER_PAGE)

icon_rebuild_index_instances = Icon(FOLDER_PAGE)

icon_folder = Icon(FOLDER)
icon_folder_with_document = Icon(FOLDER_PAGE)
icon_next_level = Icon(BULLET_GO)
