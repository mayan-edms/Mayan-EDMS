from __future__ import absolute_import

from django.db import models
from django.db.models import Q

from documents.models import Document

from .literals import INCLUSION_AND, INCLUSION_OR


class SmartLinkManager(models.Manager):
    def get_for(self, document, smart_link_obj=None):
        errors = []
        result = {}

        smart_link_qs = self.model.objects.filter(enabled=True)

        if smart_link_obj:
            smart_link_qs = smart_link_qs.filter(pk=smart_link_obj.pk)

        smart_link_qs = smart_link_qs.filter(document_types=document.document_type)

        for smart_link in smart_link_qs:
            total_query = Q()
            for condition in smart_link.smartlinkcondition_set.filter(enabled=True):
                value_query = Q(**{
                    '%s__%s' % (condition.foreign_document_data, condition.operator): eval(condition.expression, {'document': document})
                })
                if condition.negated:
                    query = ~value_query
                else:
                    query = value_query
                if condition.inclusion == INCLUSION_AND:
                    total_query &= query
                elif condition.inclusion == INCLUSION_OR:
                    total_query |= query

            if total_query:
                try:
                    document_qs = Document.objects.filter(total_query)
                    result[smart_link] = {'documents': document_qs.order_by('date_added') or []}
                except Exception as exception:
                    result[smart_link] = {'documents': []}
                    errors.append(exception)
            else:
                result[smart_link] = {'documents': []}

            if smart_link.dynamic_title:
                try:
                    result[smart_link]['title'] = eval(smart_link.dynamic_title, {'document': document})
                except Exception as exception:
                    result[smart_link]['title'] = 'Error; %s' % exception
            else:
                result[smart_link]['title'] = smart_link.title

        if smart_link_obj:
            # Return a single group if documents even if there were
            # many matches
            return result[smart_link_obj], errors

        return result, errors
