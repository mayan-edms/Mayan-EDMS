from __future__ import unicode_literals

from django.template import Template, Context


class Icon(object):
    templates = {
        'classes': '<i class="hidden-xs hidden-sm hidden-md {{ classes }}"></i>',
        'symbol': '<i class="hidden-xs hidden-sm hidden-md fa fa-{{ symbol }}"></i>'
    }

    def __init__(self, classes=None, symbol=None):
        self.classes = classes
        self.symbol = symbol

        if self.classes:
            self.template = self.templates['classes']
        else:
            self.template = self.templates['symbol']

    def render(self):
        return Template(self.template).render(
            context=Context(
                {
                    'classes': self.classes,
                    'symbol': self.symbol,
                }
            )
        )
