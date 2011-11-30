from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.template.defaultfilters import slugify

from documents.models import Document
from metadata.classes import MetadataObject

from document_indexing.models import Index, IndexInstance, \
    DocumentRenameCount
from document_indexing.conf.settings import AVAILABLE_INDEXING_FUNCTIONS
from document_indexing.conf.settings import MAX_SUFFIX_COUNT
from document_indexing.filesystem import fs_create_index_directory, \
    fs_create_document_link, fs_delete_document_link, \
    fs_delete_index_directory, fs_delete_directory_recusive
from document_indexing.conf.settings import SLUGIFY_PATHS
from document_indexing.os_agnostic import assemble_document_filename

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

    for root in Index.objects.filter(parent=None):
        index_warnings = _evaluate_index(eval_dict, document, root)
        warnings.extend(index_warnings)

    return warnings


def delete_indexes(document):
    """
    Delete all the index instances related to a document
    """
    warnings = []

    for index_instance in document.indexinstance_set.all():
        index_warnings = _remove_document_from_index_instance(document, index_instance)
        warnings.extend(index_warnings)

    return warnings


def get_instance_link(index_instance=None, text=None, simple=False):
    """
    Return an HTML anchor to an index instance
    """

    if simple:
        # Just display the instance's value or overrided text, no
        # HTML anchor
        template = u'%(value)s'
    else:
        template = u'<a href="%(url)s">%(value)s</a>'
    if index_instance:
        return template % {
            'url': index_instance.get_absolute_url(),
            'value': text if text else index_instance
        }
    else:
        # Root node
        return template % {
            'url': reverse('index_instance_list'),
            'value': ugettext(u'root')
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

    result.append(get_instance_link(simple=simple))

    for instance in index_instance.get_ancestors():
        result.append(get_instance_link(instance, simple=simple))

    result.append(get_instance_link(index_instance, simple=simple))

    output = []

    if include_count:
        output.append(u'(%d)' % index_instance.documents.count())

    if single_link:
        # Return the entire breadcrumb path as a single HTML anchor
        output.insert(0, get_instance_link(index_instance=index_instance, text=(u' / '.join(result))))
        return mark_safe(u' '.join(output))
    else:
        output.insert(0, u' / '.join(result))
        return mark_safe(u' '.join(output))


def do_rebuild_all_indexes():
    fs_delete_directory_recusive()
    IndexInstance.objects.all().delete()
    DocumentRenameCount.objects.all().delete()
    for document in Document.objects.all():
        update_indexes(document)

    return []  # Warnings - None


# Internal functions
def find_lowest_available_suffix(index_instance, document):
    # TODO: verify extension's role in query
    index_instance_documents = DocumentRenameCount.objects.filter(index_instance=index_instance)#.filter(document__file_extension=document.file_extension)
    files_list = []
    for index_instance_document in index_instance_documents:
        files_list.append(assemble_document_filename(index_instance_document.document, index_instance_document.suffix))

    for suffix in xrange(MAX_SUFFIX_COUNT):
        if assemble_document_filename(document, suffix) not in files_list:
            return suffix

    raise MaxSuffixCountReached(ugettext(u'Maximum suffix (%s) count reached.') % MAX_SUFFIX_COUNT)


def _evaluate_index(eval_dict, document, node, parent_index_instance=None):
    """
    Evaluate an enabled index expression and update or create all the
    related index instances also recursively calling itself to evaluate
    all the index's children
    """
    warnings = []
    if node.enabled:
        try:
            result = eval(node.expression, eval_dict, AVAILABLE_INDEXING_FUNCTIONS)
            if result:
                index_instance, created = IndexInstance.objects.get_or_create(index=node, value=result, parent=parent_index_instance)
                #if created:
                fs_create_index_directory(index_instance)
                if node.link_documents:
                    suffix = find_lowest_available_suffix(index_instance, document)
                    document_count = DocumentRenameCount(
                        index_instance=index_instance,
                        document=document,
                        suffix=suffix
                    )
                    document_count.save()

                    fs_create_document_link(index_instance, document, suffix)
                    index_instance.documents.add(document)

                for children in node.get_children():
                    children_warnings = _evaluate_index(
                        eval_dict, document, children, index_instance
                    )
                    warnings.extend(children_warnings)

        except (NameError, AttributeError), exc:
            warnings.append(_(u'Error in document indexing update expression: %(expression)s; %(exception)s') % {
                'expression': node.expression, 'exception': exc})
        except Exception, exc:
            warnings.append(_(u'Error updating document index, expression: %(expression)s; %(exception)s') % {
                'expression': node.expression, 'exception': exc})

    return warnings


def _remove_document_from_index_instance(document, index_instance):
    """
    Delete a documents reference from an index instance and call itself
    recusively deleting documents and empty index instances up to the
    root of the tree
    """
    warnings = []
    try:
        document_rename_count = DocumentRenameCount.objects.get(index_instance=index_instance, document=document)
        fs_delete_document_link(index_instance, document, document_rename_count.suffix)
        document_rename_count.delete()
        index_instance.documents.remove(document)
        if index_instance.documents.count() == 0 and index_instance.get_children().count() == 0:
            # if there are no more documents and no children, delete
            # node and check parent for the same conditions
            parent = index_instance.parent
            fs_delete_index_directory(index_instance)
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
