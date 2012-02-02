from __future__ import absolute_import

from django.db import models
from django.db.models import Q

from metadata.classes import MetadataClass
from documents.models import Document

from .literals import INCLUSION_AND, INCLUSION_OR


class SmartLinkManager(models.Manager):
    def get_smart_link_instances_for(self, document, smart_link_obj=None):
        errors = []
        result = {}
        metadata_dict = {}
        for document_metadata in document.documentmetadata_set.all():
            metadata_dict[document_metadata.metadata_type.name] = document_metadata.value
        eval_dict = {}
        eval_dict['document'] = document
        eval_dict['metadata'] = MetadataClass(metadata_dict)

        if smart_link_obj:
            smart_link_qs = self.model.objects.filter(Q(enabled=True) & Q(pk=smart_link_obj.pk))
        else:
            smart_link_qs = self.model.objects.filter(enabled=True)

        for smart_link in smart_link_qs:
            total_query = Q()
            for condition in smart_link.smartlinkcondition_set.filter(enabled=True):
                cls, attribute = condition.foreign_document_data.lower().split(u'.')
                try:
                    if cls == u'metadata':
                        value_query = Q(**{'documentmetadata__value__%s' % condition.operator: eval(condition.expression, eval_dict)})
                        if condition.negated:
                            query = (Q(documentmetadata__metadata_type__name=attribute) & ~value_query)
                        else:
                            query = (Q(documentmetadata__metadata_type__name=attribute) & value_query)
                        if condition.inclusion == INCLUSION_AND:
                            total_query &= query
                        elif condition.inclusion == INCLUSION_OR:
                            total_query |= query

                    elif cls == u'document':
                        value_query = Q(**{
                            '%s__%s' % (attribute, condition.operator): eval(condition.expression, eval_dict)
                        })
                        if condition.negated:
                            query = ~value_query
                        else:
                            query = value_query
                        if condition.inclusion == INCLUSION_AND:
                            total_query &= query
                        elif condition.inclusion == INCLUSION_OR:
                            total_query |= query

                except Exception, e:
                    errors.append(e)
                    value_query = Q()
                    query = Q()
            if total_query:
                try:
                    document_qs = Document.objects.filter(total_query)
                    result[smart_link] = {'documents': document_qs.order_by('date_added') or []}
                except Exception, e:
                    result[smart_link] = {'documents': []}
                    errors.append(e)
            else:
                result[smart_link] = {'documents': []}

            if smart_link.dynamic_title:
                try:
                    result[smart_link]['title'] = eval(smart_link.dynamic_title, eval_dict)
                except Exception, e:
                    result[smart_link]['title'] = 'Error; %s' % e
            else:
                result[smart_link]['title'] = smart_link.title

        if smart_link_obj:
            # Return a single group if documents even if there were
            # many matches
            return result[smart_link_obj], errors

        return result, errors
