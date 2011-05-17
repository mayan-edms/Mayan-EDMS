from django.utils.translation import ugettext_lazy as _

from metadata.classes import MetadataObject

#from filesystem_serving.conf.settings import MAX_RENAME_COUNT

from document_indexing.models import Index, IndexInstance
from document_indexing.conf.settings import AVAILABLE_INDEXING_FUNCTIONS


def evaluate_index(eval_dict, document, node, parent_index_instance=None):
    warnings = []
    if node.enabled:
        try:
            result = eval(node.expression, eval_dict, AVAILABLE_INDEXING_FUNCTIONS)
            index_instance, created = IndexInstance.objects.get_or_create(index=node, value=result, parent=parent_index_instance)
            if node.link_document:
                index_instance.documents.add(document)
                
            for children in node.get_children():
                children_warnings = evaluate_index(eval_dict, document, children, index_instance)
                warnings.extend(children_warnings)
            
        except NameError, exc:
            warnings.append(_(u'Error in metadata indexing expression: %s') % exc)
            #raise NameError()
            #This should be a warning not an error
            #pass
        except Exception, exc:
            warnings.append(_(u'Unable to create metadata indexing directory: %s') % exc)
            
    return warnings


def update_indexes(document):
    print 'update_indexes'
    warnings = []

    eval_dict = {}
    eval_dict['document'] = document
    metadata_dict = dict([(metadata.metadata_type.name, metadata.value) for metadata in document.documentmetadata_set.all() if metadata.value])
    eval_dict['metadata'] = MetadataObject(metadata_dict)

    for root in Index.objects.filter(parent=None):
        #for node in root.get_children():
        index_warnings = evaluate_index(eval_dict, document, root)
        warnings.extend(index_warnings)

    return warnings
    
    
def delete_indexes(document):
    print 'delete_indexes'
