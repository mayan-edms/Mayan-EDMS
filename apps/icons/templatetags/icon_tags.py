from django.template import Library

from icons import Icon

register = Library()


@register.simple_tag
def icon_small(icon_name):
    return Icon(icon_name).display_small()


@register.simple_tag
def icon_big(icon_name):
    return Icon(icon_name).display_big()
