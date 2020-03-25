from django.apps import apps
from django.utils.encoding import force_text
from django.utils.html import mark_safe, escape

from .icons import (
    icon_index, icon_index_level_up, icon_index_instance_node_with_documents
)


def get_instance_link(index_instance_node):
    """
    Return an HTML anchor to an index node instance
    """
    return mark_safe(
        s='<a href="{url}">{text}</a>'.format(
            url=index_instance_node.get_absolute_url(),
            text=escape(index_instance_node.get_full_path())
        )
    )


def index_instance_item_link(index_instance_item):
    IndexInstanceNode = apps.get_model(
        app_label='document_indexing', model_name='IndexInstanceNode'
    )

    if isinstance(index_instance_item, IndexInstanceNode):
        if index_instance_item.index_template_node.link_documents:
            icon = icon_index_instance_node_with_documents.render()
        else:
            icon = icon_index_level_up.render()
    else:
        icon = ''

    return mark_safe(
        s='%(icon)s&nbsp;<a href="%(url)s">%(text)s</a>' % {
            'url': index_instance_item.get_absolute_url(),
            'icon': icon,
            'text': index_instance_item
        }
    )


def node_level(node):
    """
    Render an indented tree like output for a specific node
    """
    return mark_safe(
        s=''.join(
            [
                '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' * node.get_level(),
                '' if node.is_root_node() else icon_index_level_up.render(),
                force_text(node)
            ]
        )
    )


def node_tree(node, user):
    result = []

    result.append('<div class="list-group">')

    for ancestor in node.get_ancestors(include_self=True):
        if ancestor.is_root_node():
            element = node.index()
            icon = icon_index
        else:
            element = ancestor
            if element.index_template_node.link_documents:
                icon = icon_index_instance_node_with_documents
            else:
                icon = icon_index_level_up

        result.append(
            '<a href="{url}" class="list-group-item {active}"><span class="badge">{count}</span>{icon} {text}</a>'.format(
                url=element.get_absolute_url(),
                active='active' if element == node or node.get_ancestors(include_self=True).count() == 1 else '',
                count=element.get_item_count(user=user),
                icon=icon.render(),
                text=escape(element)
            )
        )

    result.append('</div>')

    return mark_safe(''.join(result))
