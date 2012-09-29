from django.template import Library

from common.icons import (icon_tick, icon_cross, icon_resultset_previous, icon_current_user_details)

register = Library()


@register.simple_tag(takes_context=True)
def default_icons(context):
    context['icon_submit_default'] = icon_tick
    context['icon_cancel_default'] = icon_cross
    context['icon_current_link'] = icon_resultset_previous
    context['icon_current_user_details'] = icon_current_user_details
    return u''
