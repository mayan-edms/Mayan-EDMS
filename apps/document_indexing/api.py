from __future__ import absolute_import

from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.template.defaultfilters import slugify

from metadata.classes import MetadataClass

from .models import Index, IndexInstanceNode, DocumentRenameCount
from .conf.settings import (AVAILABLE_INDEXING_FUNCTIONS,
    MAX_SUFFIX_COUNT, SLUGIFY_PATHS)
from .filesystem import (fs_create_index_directory,
    fs_create_document_link, fs_delete_document_link,
    fs_delete_index_directory, assemble_suffixed_filename)
from .exceptions import MaxSuffixCountReached

if SLUGIFY_PATHS == False:
    # Do not slugify path or filenames and extensions
    SLUGIFY_FUNCTION = lambda x: x
else:
    SLUGIFY_FUNCTION = slugify


# External functions
def update_indexes(document):
    """
    Update or create all the index instances related to a document
    """
    warnings = []

    eval_dict = {}
    document_metadata_dict = dict([(metadata.metadata_type.name, metadata.value) for metadata in document.documentmetadata_set.all() if metadata.value])
    eval_dict['document'] = document
    eval_dict['metadata'] = MetadataClass(document_metadata_dict)

    # Only update indexes where the document type is found or that do not have any document type specified
    for index in Index.objects.filter(Q(enabled=True) & (Q(document_types=None) | Q(document_types=document.document_type))):
        root_instance, created = IndexInstanceNode.objects.get_or_create(index_template_node=index.template_root, parent=None)
        for template_node in index.template_root.get_children():
            index_warnings = cascade_eval(eval_dict, document, template_node, root_instance)
            warnings.extend(index_warnings)

    return warnings


def delete_indexes(document):
    """
    Delete all the index instances related to a document
    """
    warnings = []

    for index_instance in document.indexinstancenode_set.all():
        index_warnings = cascade_document_remove(document, index_instance)
        warnings.extend(index_warnings)

    return warnings


# Internal functions
def find_lowest_available_suffix(index_instance, document):
    index_instance_documents = DocumentRenameCount.objects.filter(index_instance_node=index_instance)
    files_list = []
    for index_instance_document in index_instance_documents:
        files_list.append(assemble_suffixed_filename(index_instance_document.document.file_filename, index_instance_document.suffix))

    for suffix in xrange(MAX_SUFFIX_COUNT):
        if assemble_suffixed_filename(document.file_filename, suffix) not in files_list:
            return suffix

    raise MaxSuffixCountReached(ugettext(u'Maximum suffix (%s) count reached.') % MAX_SUFFIX_COUNT)


def cascade_eval(eval_dict, document, template_node, parent_index_instance=None):
    """
    Evaluate an enabled index expression and update or create all the
    related index instances also recursively calling itself to evaluate
    all the index's children
    """
    warnings = []
    if template_node.enabled:
        try:
            result = eval(template_node.expression, eval_dict, AVAILABLE_INDEXING_FUNCTIONS)
        except Exception, exc:
            warnings.append(_(u'Error in document indexing update expression: %(expression)s; %(exception)s') % {
                'expression': template_node.expression, 'exception': exc})
        else:
            if result:
                index_instance, created = IndexInstanceNode.objects.get_or_create(index_template_node=template_node, value=result, parent=parent_index_instance)
                #if created:
                try:
                    fs_create_index_directory(index_instance)
                except Exception, exc:
                    warnings.append(_(u'Error updating document index, expression: %(expression)s; %(exception)s') % {
                        'expression': template_node.expression, 'exception': exc})

                if template_node.link_documents:
                    suffix = find_lowest_available_suffix(index_instance, document)
                    document_count = DocumentRenameCount(
                        index_instance_node=index_instance,
                        document=document,
                        suffix=suffix
                    )
                    document_count.save()

                    try:
                        fs_create_document_link(index_instance, document, suffix)
                    except Exception, exc:
                        warnings.append(_(u'Error updating document index, expression: %(expression)s; %(exception)s') % {
                            'expression': template_node.expression, 'exception': exc})

                    index_instance.documents.add(document)

                for child in template_node.get_children():
                    children_warnings = cascade_eval(
                        eval_dict=eval_dict,
                        document=document,
                        template_node=child,
                        parent_index_instance=index_instance
                    )
                    warnings.extend(children_warnings)

    return warnings


def cascade_document_remove(document, index_instance):
    """
    Delete a documents reference from an index instance and call itself
    recusively deleting documents and empty index instances up to the
    root of the tree
    """
    warnings = []
    try:
        document_rename_count = DocumentRenameCount.objects.get(index_instance_node=index_instance, document=document)
        fs_delete_document_link(index_instance, document, document_rename_count.suffix)
        document_rename_count.delete()
        index_instance.documents.remove(document)
        if index_instance.documents.count() == 0 and index_instance.get_children().count() == 0:
            # if there are no more documents and no children, delete
            # node and check parent for the same conditions
            parent = index_instance.parent
            fs_delete_index_directory(index_instance)
            index_instance.delete()
            parent_warnings = cascade_document_remove(
                document, parent
            )
            warnings.extend(parent_warnings)
    except DocumentRenameCount.DoesNotExist:
        return warnings
    except Exception, exc:
        warnings.append(_(u'Unable to delete document indexing node; %s') % exc)

    return warnings
