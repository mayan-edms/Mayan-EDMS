# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.html import mark_safe
from django.utils.translation import ugettext

from .models import IndexInstanceNode


def get_instance_link(index_instance_node, text=None, simple=False):
    """
    Return an HTML anchor to an index instance
    """

    if simple:
        # Just display the instance's value or overrided text, no
        # HTML anchor
        template = '%(value)s'
    else:
        template = '<a href="%(url)s">%(value)s</a>'

    return template % {
        'url': index_instance_node.get_absolute_url(),
        'value': text if text else (
            index_instance_node if index_instance_node.parent else index_instance_node.index_template_node.index
        )
    }


def get_breadcrumbs(index_instance_node, simple=False, single_link=False, include_count=False):
    """
    Return a joined string of HTML anchors to every index instance's
    parent from the root of the tree to the index instance
    """

    result = []
    if single_link:
        # Return the entire breadcrumb path as a single HTML anchor
        simple = True

    for instance in index_instance_node.get_ancestors():
        result.append(get_instance_link(instance, simple=simple))

    result.append(get_instance_link(index_instance_node, simple=simple))

    output = []

    if include_count:
        output.append('(%d)' % index_instance_node.documents.count())

    if single_link:
        # Return the entire breadcrumb path as a single HTML anchor
        output.insert(
            0, get_instance_link(
                index_instance_node=index_instance_node, text=(
                    ' / '.join(result)
                )
            )
        )
        return mark_safe(' '.join(output))
    else:
        output.insert(0, ' / '.join(result))
        return mark_safe(' '.join(output))


def index_instance_item_link(index_instance_item):
    if isinstance(index_instance_item, IndexInstanceNode):
        if index_instance_item.index_template_node.link_documents:
            icon_template = '<i class="fa fa-folder"></i>'
        else:
            icon_template = '<i class="fa fa-level-up fa-rotate-90"></i>'
    else:
        icon_template = ''

    return mark_safe(
        '%(icon_template)s&nbsp;<a href="%(url)s">%(text)s</a>' % {
            'url': index_instance_item.get_absolute_url(),
            'icon_template': icon_template,
            'text': index_instance_item
        }
    )


def node_level(node):
    """
    Render an indented tree like output for a specific node
    """

    return mark_safe(
        ''.join(
            [
                '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' * (
                    getattr(node, node._mptt_meta.level_attr) - 1
                ), '' if node.is_root_node() else '<i class="fa fa-level-up fa-rotate-90"></i> ',
                ugettext('Root') if node.is_root_node() else unicode(node)
            ]
        )
    )
