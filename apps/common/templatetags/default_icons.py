from django.template import Library

from common.icons import icon_tick, icon_cross

register = Library()


@register.simple_tag(takes_context=True)
def default_icons(context):
    context['submit_icon_default'] = icon_tick
    context['cancel_icon_default'] = icon_cross
    return u''
