from django.db import models

#from documents.models import DocumentGroup
from metadata.classes import MetadataObject


class DocumentGroupManager(models.Manager):
    def get_groups_for(self, document, group_obj=None):
        errors = []
        metadata_groups = {}
        metadata_dict = {}
        for document_metadata in document.documentmetadata_set.all():
            metadata_dict[document_metadata.metadata_type.name] = document_metadata.value
        eval_dict = {}
        eval_dict['document'] = document
        eval_dict['metadata'] = MetadataObject(metadata_dict)
        
        #if group_obj:
        #    groups_qs = DocumentGroup.objects.filter((Q(document_type=document.document_type) | Q(document_type=None)) & Q(enabled=True) & Q(pk=group_obj.pk))
        #else:
        #    groups_qs = DocumentGroup.objects.filter((Q(document_type=document.document_type) | Q(document_type=None)) & Q(enabled=True))
        groups_qs=[]

        for group in groups_qs:
            total_query = Q()
            for item in group.metadatagroupitem_set.filter(enabled=True):
                try:
                    value_query = Q(**{'value__%s' % item.operator: eval(item.expression, eval_dict)})
                    if item.negated:
                        query = (Q(metadata_type__id=item.metadata_type_id) & ~value_query)
                    else:
                        query = (Q(metadata_type__id=item.metadata_type_id) & value_query)

                    if item.inclusion == INCLUSION_AND:
                        total_query &= query
                    elif item.inclusion == INCLUSION_OR:
                        total_query |= query
                except Exception, e:
                    errors.append(e)
                    value_query = Q()
                    query = Q()

            if total_query:
                document_id_list = DocumentMetadata.objects.filter(total_query).values_list('document', flat=True)
                metadata_groups[group] = Document.objects.filter(Q(id__in=document_id_list)).order_by('file_filename') or []
            else:
                metadata_groups[group] = []

        if group_obj:
            return metadata_groups[group_obj], errors

        return metadata_groups, errors
