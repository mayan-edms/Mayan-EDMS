from django.db import models
from django.db.models import Q

from metadata.classes import MetadataObject
from documents.models import Document

from grouping.literals import INCLUSION_AND, INCLUSION_OR


class DocumentGroupManager(models.Manager):
    def get_groups_for(self, document, group_obj=None):
        errors = []
        document_groups = {}
        metadata_dict = {}
        for document_metadata in document.documentmetadata_set.all():
            metadata_dict[document_metadata.metadata_type.name] = document_metadata.value
        eval_dict = {}
        eval_dict['document'] = document
        eval_dict['metadata'] = MetadataObject(metadata_dict)

        if group_obj:
            groups_qs = self.model.objects.filter(Q(enabled=True) & Q(pk=group_obj.pk))
        else:
            groups_qs = self.model.objects.filter(enabled=True)

        for group in groups_qs:
            total_query = Q()
            for item in group.documentgroupitem_set.filter(enabled=True):
                cls, attribute = item.foreign_document_data.lower().split(u'.')
                try:
                    if cls == u'metadata':
                        value_query = Q(**{'documentmetadata__value__%s' % item.operator: eval(item.expression, eval_dict)})
                        if item.negated:
                            query = (Q(documentmetadata__metadata_type__name=attribute) & ~value_query)
                        else:
                            query = (Q(documentmetadata__metadata_type__name=attribute) & value_query)
                        if item.inclusion == INCLUSION_AND:
                            total_query &= query
                        elif item.inclusion == INCLUSION_OR:
                            total_query |= query

                    elif cls == u'document':
                        value_query = Q(**{
                            '%s__%s' % (attribute, item.operator): eval(item.expression, eval_dict)
                        })
                        if item.negated:
                            query = ~value_query
                        else:
                            query = value_query
                        if item.inclusion == INCLUSION_AND:
                            total_query &= query
                        elif item.inclusion == INCLUSION_OR:
                            total_query |= query

                except Exception, e:
                    errors.append(e)
                    value_query = Q()
                    query = Q()
            if total_query:
                try:
                    document_qs = Document.objects.filter(total_query)
                    document_groups[group] = {'documents': document_qs.order_by('file_filename') or []}
                except Exception, e:
                    document_groups[group] = {'documents': []}
                    errors.append(e)
            else:
                document_groups[group] = {'documents': []}

            if group.dynamic_title:
                try:
                    document_groups[group]['title'] = eval(group.dynamic_title, eval_dict)
                except Exception, e:
                    document_groups[group]['title'] = 'Error; %s' % e
            else:
                document_groups[group]['title'] = group.title

        if group_obj:
            # Return a single group if documents even if there were
            # many matches
            return document_groups[group_obj], errors

        return document_groups, errors
