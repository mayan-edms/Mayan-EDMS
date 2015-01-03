from __future__ import absolute_import

import logging

from django.db.models import Q
from django.utils.translation import ugettext
from django.utils.translation import ugettext_lazy as _

from .models import Index, IndexInstanceNode
from .settings import AVAILABLE_INDEXING_FUNCTIONS

logger = logging.getLogger(__name__)


# External functions
def update_indexes(document):
    """
    Update or create all the index instances related to a document
    """
    # TODO: convert this fuction into a manager method

    warnings = []

    # Only update indexes where the document type is found or that do not have any document type specified
    for index in Index.objects.filter(Q(enabled=True) & (Q(document_types=None) | Q(document_types=document.document_type))):
        root_instance, created = IndexInstanceNode.objects.get_or_create(index_template_node=index.template_root, parent=None)
        for template_node in index.template_root.get_children():
            index_warnings = cascade_eval(document, template_node, root_instance)
            warnings.extend(index_warnings)

    return warnings


# Internal functions
def find_lowest_available_suffix(index_instance, document):
    index_instance_documents = DocumentRenameCount.objects.filter(index_instance_node=index_instance)
    files_list = []
    for index_instance_document in index_instance_documents:
        files_list.append(assemble_suffixed_filename(index_instance_document.document.label, index_instance_document.suffix))

    for suffix in xrange(MAX_SUFFIX_COUNT):
        if assemble_suffixed_filename(document.label, suffix) not in files_list:
            return suffix

    raise MaxSuffixCountReached(ugettext(u'Maximum suffix (%s) count reached.') % MAX_SUFFIX_COUNT)


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
            error_message = _(u'Error indexing document: %(document)s; expression: %(expression)s; %(exception)s') % {
                'document': document, 'expression': template_node.expression, 'exception': exception}
            warnings.append(error_message)
            logger.debug(error_message)
        else:
            if result:
                index_instance, created = IndexInstanceNode.objects.get_or_create(index_template_node=template_node, value=result, parent=parent_index_instance)

                if template_node.link_documents:
                    suffix = find_lowest_available_suffix(index_instance, document)
                    document_count = DocumentRenameCount(
                        index_instance_node=index_instance,
                        document=document,
                        suffix=suffix
                    )
                    document_count.save()
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

    for instance_node in IndexInstanceNode.objects.filter(documents__isnull=True):
        task_delete_empty_index_nodes_recursive(instance_node)



def task_delete_empty_index_nodes_recursive(instance_node):
    """
    Calls itself recursively deleting empty index instance nodes up to root
    """

    if instance_node.get_children().count() == 0:
        # if there are no children, delete node and check parent for the
        # same conditions
        parent = instance_node.parent
        instance_node.delete()
        delete_empty_indexes(parent)
