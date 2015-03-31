from __future__ import unicode_literals

from django.template import Library

register = Library()


@register.filter
def get_choice_value(field):
    try:
        return dict(field.field.choices)[field.value()]
    except TypeError:
        return ', '.join([entry for id, entry in field.field.choices])
