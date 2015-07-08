from __future__ import unicode_literals

from django.db import models
from django.db.models import Q
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from documents.models import Document, DocumentType

from .literals import (
    INCLUSION_AND, INCLUSION_CHOICES, INCLUSION_OR, OPERATOR_CHOICES
)


@python_2_unicode_compatible
class SmartLink(models.Model):
    label = models.CharField(max_length=96, verbose_name=_('Label'))
    dynamic_label = models.CharField(blank=True, max_length=96, verbose_name=_('Dynamic label'), help_text=_('This expression will be evaluated against the current selected document.'))
    enabled = models.BooleanField(default=True, verbose_name=_('Enabled'))
    document_types = models.ManyToManyField(DocumentType, verbose_name=_('Document types'))

    def __str__(self):
        return self.label

    def get_dynamic_label(self, document):
        if self.dynamic_label:
            try:
                return eval(self.dynamic_label, {'document': document})
            except Exception as exception:
                return Exception(_('Error generating dynamic label; %s' % unicode(exception)))
        else:
            return self.label

    def resolve_for(self, document):
        return ResolvedSmartLink(smart_link=self, queryset=self.get_linked_document_for(document))

    def get_linked_document_for(self, document):
        if document.document_type.pk not in self.document_types.values_list('pk', flat=True):
            raise Exception(_('This smart link is not allowed for the selected document\'s type.'))

        smart_link_query = Q()

        for condition in self.conditions.filter(enabled=True):
            condition_query = Q(**{
                '%s__%s' % (condition.foreign_document_data, condition.operator): eval(condition.expression, {'document': document})
            })
            if condition.negated:
                condition_query = ~condition_query

            if condition.inclusion == INCLUSION_AND:
                smart_link_query &= condition_query
            elif condition.inclusion == INCLUSION_OR:
                smart_link_query |= condition_query

        if smart_link_query:
            return Document.objects.filter(smart_link_query)
        else:
            return Document.objects.none()

    class Meta:
        verbose_name = _('Smart link')
        verbose_name_plural = _('Smart links')


class ResolvedSmartLink(SmartLink):
    class Meta:
        proxy = True


@python_2_unicode_compatible
class SmartLinkCondition(models.Model):
    smart_link = models.ForeignKey(SmartLink, related_name='conditions', verbose_name=_('Smart link'))
    inclusion = models.CharField(default=INCLUSION_AND, max_length=16, choices=INCLUSION_CHOICES, help_text=_('The inclusion is ignored for the first item.'))
    foreign_document_data = models.CharField(max_length=128, verbose_name=_('Foreign document attribute'), help_text=_('This represents the metadata of all other documents.'))
    operator = models.CharField(max_length=16, choices=OPERATOR_CHOICES)
    expression = models.TextField(verbose_name=_('Expression'), help_text=_('This expression will be evaluated against the current document.'))
    negated = models.BooleanField(default=False, verbose_name=_('Negated'), help_text=_('Inverts the logic of the operator.'))
    enabled = models.BooleanField(default=True, verbose_name=_('Enabled'))

    def __str__(self):
        return '%s foreign %s %s %s %s' % (self.get_inclusion_display(), self.foreign_document_data, _('not') if self.negated else '', self.get_operator_display(), self.expression)

    class Meta:
        verbose_name = _('Link condition')
        verbose_name_plural = _('Link conditions')
