from django.utils.translation import ugettext_lazy as _

INCLUSION_AND = u'&'
INCLUSION_OR = u'|'

INCLUSION_CHOICES = (
    (INCLUSION_AND, _(u'and')),
    (INCLUSION_OR, _(u'or')),
)

OPERATOR_CHOICES = (
    (u'exact', _(u'is equal to')),
    (u'iexact', _(u'is equal to (case insensitive)')),
    (u'contains', _(u'contains')),
    (u'icontains', _(u'contains (case insensitive)')),
    (u'in', _(u'is in')),
    (u'gt', _(u'is greater than')),
    (u'gte', _(u'is greater than or equal to')),
    (u'lt', _(u'is less than')),
    (u'lte', _(u'is less than or equal to')),
    (u'startswith', _(u'starts with')),
    (u'istartswith', _(u'starts with (case insensitive)')),
    (u'endswith', _(u'ends with')),
    (u'iendswith', _(u'ends with (case insensitive)')),
    (u'regex', _(u'is in regular expression')),
    (u'iregex', _(u'is in regular expression (case insensitive)')),
)
