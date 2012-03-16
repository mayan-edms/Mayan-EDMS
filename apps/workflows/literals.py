from django.utils.translation import ugettext_lazy as _

OPERAND_OR = 'or'
OPERAND_AND = 'and'

OPERAND_CHOICES = (
    (OPERAND_OR, _(u'or')),
    (OPERAND_AND, _(u'and'))
)
