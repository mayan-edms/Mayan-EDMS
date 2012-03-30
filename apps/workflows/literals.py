from django.utils.translation import ugettext_lazy as _

OPERAND_OR = 'or'
OPERAND_AND = 'and'

OPERAND_CHOICES = (
    (OPERAND_OR, _(u'or')),
    (OPERAND_AND, _(u'and'))
)

NODE_TYPE_TASK = 'task'
NODE_TYPE_START = 'start'
NODE_TYPE_END = 'end'

NODE_TYPE_CHOICES = (
    (NODE_TYPE_TASK, _(u'Simple task')),
    (NODE_TYPE_START, _(u'Start')),
    (NODE_TYPE_END, _(u'End')),
)
