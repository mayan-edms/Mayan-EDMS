from __future__ import unicode_literals

from django.template import Library

from common.utils import urlquote

from ..classes import Menu
from ..forms import MultiItemForm

register = Library()


@register.assignment_tag(takes_context=True)
def get_menu_links(context, name, source=None):
    return Menu.get(name).resolve(context=context, source=source)


@register.assignment_tag(takes_context=True)
def get_menus_links(context, names, source=None):
    result = []

    for name in names.split(','):
        links = Menu.get(name=name).resolve(context)
        if links:
            result.append(links)

    return result


@register.simple_tag(takes_context=True)
def get_multi_item_links_form(context, object_list):
    actions = [(link.url, link.text) for link in Menu.get('multi item menu').resolve(context=context, source=object_list[0])]
    form = MultiItemForm(actions=actions)
    context.update({'multi_item_form': form, 'multi_item_actions': actions})
    return ''
