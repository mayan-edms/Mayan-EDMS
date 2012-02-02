from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.template.defaultfilters import slugify

from documents.models import Document
from metadata.classes import MetadataObject

from .models import (Index, IndexTemplateNode, IndexInstanceNode,
    DocumentRenameCount)
from .conf.settings import (AVAILABLE_INDEXING_FUNCTIONS,
    MAX_SUFFIX_COUNT, SLUGIFY_PATHS)
from .filesystem import (fs_create_index_directory,
    fs_create_document_link, fs_delete_document_link,
    fs_delete_index_directory, fs_delete_directory_recusive)
from .os_specifics import assemble_suffixed_filename

if SLUGIFY_PATHS == False:
    # Do not slugify path or filenames and extensions
    SLUGIFY_FUNCTION = lambda x: x
else:
    SLUGIFY_FUNCTION = slugify


class MaxSuffixCountReached(Exception):
    pass


# External functions
def update_indexes(document):
    """
    Update or create all the index instances related to a document
    """
    warnings = []

    eval_dict = {}
    document_metadata_dict = dict([(metadata.metadata_type.name, metadata.value) for metadata in document.documentmetadata_set.all() if metadata.value])
    eval_dict['document'] = document
    eval_dict['metadata'] = MetadataObject(document_metadata_dict)

    for index in Index.objects.filter(enabled=True):
        root_instance, created = IndexInstanceNode.objects.get_or_create(index_template_node=index.template_root, parent=None)
        for template_node in index.template_root.get_children():
            index_warnings = _evaluate_index(eval_dict, document, template_node, root_instance)
            warnings.extend(index_warnings)

    return warnings


def delete_indexes(document):
    """
    Delete all the index instances related to a document
    """
    warnings = []

    for index_instance in document.indexinstancenode_set.all():
        index_warnings = _remove_document_from_index_instance(document, index_instance)
        warnings.extend(index_warnings)

    return warnings


def get_instance_link(index_instance_node, text=None, simple=False):
    """
    Return an HTML anchor to an index instance
    """

    if simple:
        # Just display the instance's value or overrided text, no
        # HTML anchor
        template = u'%(value)s'
    else:
        template = u'<a href="%(url)s">%(value)s</a>'

    return template % {
        'url': index_instance_node.get_absolute_url(),
        'value': text if text else (index_instance_node if index_instance_node.parent else index_instance_node.index_template_node.index)
    }


def get_breadcrumbs(index_instance, simple=False, single_link=False, include_count=False):
    """
    Return a joined string of HTML anchors to every index instance's
    parent from the root of the tree to the index instance
    """
    result = []
    if single_link:
        # Return the entire breadcrumb path as a single HTML anchor
        simple = True

    #result.append(get_instance_link(index_instance.get_root(), simple=simple))

    for instance in index_instance.get_ancestors():
        result.append(get_instance_link(instance, simple=simple))

    result.append(get_instance_link(index_instance, simple=simple))

    output = []

    if include_count:
        output.append(u'(%d)' % index_instance.documents.count())

    if single_link:
        # Return the entire breadcrumb path as a single HTML anchor
        output.insert(0, get_instance_link(index_instance_node=index_instance, text=(u' / '.join(result))))
        return mark_safe(u' '.join(output))
    else:
        output.insert(0, u' / '.join(result))
        return mark_safe(u' '.join(output))


def do_rebuild_all_indexes():
    fs_delete_directory_recusive()
    IndexInstanceNone.objects.delete()
    DocumentRenameCount.objects.delete()
    for document in Document.objects.all():
        update_indexes(document)

    return []  # Warnings - None


# Internal functions
def find_lowest_available_suffix(index_instance, document):
    # TODO: verify extension's role in query
    index_instance_documents = DocumentRenameCount.objects.filter(index_instance_node=index_instance)#.filter(document__file_extension=document.file_extension)
    files_list = []
    for index_instance_document in index_instance_documents:
        files_list.append(assemble_suffixed_filename(index_instance_document.document.file_filename, index_instance_document.suffix))

    for suffix in xrange(MAX_SUFFIX_COUNT):
        if assemble_suffixed_filename(document.file_filename, suffix) not in files_list:
            return suffix

    raise MaxSuffixCountReached(ugettext(u'Maximum suffix (%s) count reached.') % MAX_SUFFIX_COUNT)


def _evaluate_index(eval_dict, document, template_node, parent_index_instance=None):
    """
    Evaluate an enabled index expression and update or create all the
    related index instances also recursively calling itself to evaluate
    all the index's children
    """
    warnings = []
    if template_node.enabled:
        try:
            result = eval(template_node.expression, eval_dict, AVAILABLE_INDEXING_FUNCTIONS)
            if result:
                index_instance, created = IndexInstanceNode.objects.get_or_create(index_template_node=template_node)
                index_instance.value = result
                index_instance.parent = parent_index_instance
                index_instance.save()
                #if created:
                #fs_create_index_directory(index_instance)
                if template_node.link_documents:
                    suffix = find_lowest_available_suffix(index_instance, document)
                    document_count = DocumentRenameCount(
                        index_instance_node=index_instance,
                        document=document,
                        suffix=suffix
                    )
                    document_count.save()

                    #fs_create_document_link(index_instance, document, suffix)
                    index_instance.documents.add(document)

                for child in template_node.get_children():
                    children_warnings = _evaluate_index(
                        eval_dict, document, child, index_instance
                    )
                    warnings.extend(children_warnings)

        except (NameError, AttributeError), exc:
            warnings.append(_(u'Error in document indexing update expression: %(expression)s; %(exception)s') % {
                'expression': template_node.expression, 'exception': exc})
        except Exception, exc:
            warnings.append(_(u'Error updating document index, expression: %(expression)s; %(exception)s') % {
                'expression': template_node.expression, 'exception': exc})

    return warnings


def _remove_document_from_index_instance(document, index_instance):
    """
    Delete a documents reference from an index instance and call itself
    recusively deleting documents and empty index instances up to the
    root of the tree
    """
    warnings = []
    try:
        document_rename_count = DocumentRenameCount.objects.get(index_instance_node=index_instance, document=document)
        #fs_delete_document_link(index_instance, document, document_rename_count.suffix)
        document_rename_count.delete()
        index_instance.documents.remove(document)
        if index_instance.documents.count() == 0 and index_instance.get_children().count() == 0:
            # if there are no more documents and no children, delete
            # node and check parent for the same conditions
            parent = index_instance.parent
            #fs_delete_index_directory(index_instance)
            index_instance.delete()
            parent_warnings = _remove_document_from_index_instance(
                document, parent
            )
            warnings.extend(parent_warnings)
    except DocumentRenameCount.DoesNotExist:
        return warnings
    except Exception, exc:
        warnings.append(_(u'Unable to delete document indexing node; %s') % exc)

    return warnings
