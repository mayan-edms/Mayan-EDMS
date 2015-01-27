from __future__ import unicode_literals

import logging

from django.utils.translation import ugettext_lazy as _

from .models import Index, IndexInstanceNode
from .settings import AVAILABLE_INDEXING_FUNCTIONS

logger = logging.getLogger(__name__)


# External functions
def index_document(document):
    """
    Update or create all the index instances related to a document
    """
    # TODO: convert this fuction into a manager method

    warnings = []

    for index_node in IndexInstanceNode.objects.filter(documents=document):
        index_node.documents.remove(document)

    delete_empty_index_nodes()

    # Only update indexes where the document type is found
    for index in Index.objects.filter(enabled=True, document_types=document.document_type):
        root_instance, created = IndexInstanceNode.objects.get_or_create(index_template_node=index.template_root, parent=None)
        for template_node in index.template_root.get_children():
            index_warnings = cascade_eval(document, template_node, root_instance)
            warnings.extend(index_warnings)

    return warnings


def cascade_eval(document, template_node, parent_index_instance=None):
    """
    Evaluate an enabled index expression and update or create all the
    related index instances also recursively calling itself to evaluate
    all the index's children
    """

    warnings = []
    if template_node.enabled:
        try:
            result = eval(template_node.expression, {'document': document}, AVAILABLE_INDEXING_FUNCTIONS)
        except Exception as exception:
            error_message = _('Error indexing document: %(document)s; expression: %(expression)s; %(exception)s') % {
                'document': document, 'expression': template_node.expression, 'exception': exception}
            warnings.append(error_message)
            logger.debug(error_message)
        else:
            if result:
                index_instance, created = IndexInstanceNode.objects.get_or_create(index_template_node=template_node, value=result, parent=parent_index_instance)

                if template_node.link_documents:
                    index_instance.documents.add(document)

                for child in template_node.get_children():
                    children_warnings = cascade_eval(
                        document=document,
                        template_node=child,
                        parent_index_instance=index_instance
                    )
                    warnings.extend(children_warnings)

    return warnings


def delete_empty_index_nodes():
    """
    Delete empty index instance nodes
    """

    for instance_node in IndexInstanceNode.objects.filter(documents__isnull=True, parent__isnull=False):
        task_delete_empty_index_nodes_recursive(instance_node)


def task_delete_empty_index_nodes_recursive(instance_node):
    """
    Calls itself recursively deleting empty index instance nodes up to root
    """

    if instance_node.get_children().count() == 0:
        # if there are no children, delete node and check parent for the
        # same conditions
        parent = instance_node.parent
        if parent:
            instance_node.delete()
            task_delete_empty_index_nodes_recursive(parent)
