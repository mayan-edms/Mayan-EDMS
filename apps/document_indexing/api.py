from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

from documents.models import Document
from metadata.classes import MetadataObject

from document_indexing.models import Index, IndexInstance
from document_indexing.conf.settings import AVAILABLE_INDEXING_FUNCTIONS
from document_indexing.filesystem import fs_create_index_directory


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
        _remove_document_from_index_instance(document, index_instance)
            
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
            'url': index_instance.get_absolute_url(), 'value': text if text else index_instance
        }
    else:
        # Root node
        return template % {
            'url': reverse('index_instance_list'), 'value': ugettext(u'root')
        }
        

def get_breadcrumbs(index_instance, simple=False, single_link=False):
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

    if single_link:
        # Return the entire breadcrumb path as a single HTML anchor
        return mark_safe(get_instance_link(index_instance=index_instance, text=(u' / '.join(result))))
    else:
        return mark_safe(u' / '.join(result))


def do_rebuild_all_indexes():
    IndexInstance.objects.all().delete()
    for document in Document.objects.all():
        update_indexes(document)
    
    
# Internal functions
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
            index_instance, created = IndexInstance.objects.get_or_create(index=node, value=result, parent=parent_index_instance)
            if created:
                fs_create_index_directory(index_instance)
            if node.link_documents:
                index_instance.documents.add(document)

            for children in node.get_children():
                children_warnings = _evaluate_index(eval_dict, document, children, index_instance)
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
        index_instance.documents.remove(document)
        if index_instance.documents.count() == 0 and index_instance.get_children().count() == 0:
            # if there are no more documents and no children, delete
            # node and check parent for the same conditions
            parent = index_instance.parent
            index_instance.delete()
            parent_warnings = _remove_document_from_index_instance(document, parent)
            warnings.extend(parent_warnings)
            
    except Exception, exc:
        warnings.append(_(u'Unable to delete document indexing node; %s') % exc)

    return warnings
