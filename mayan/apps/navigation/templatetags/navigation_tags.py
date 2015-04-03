from __future__ import unicode_literals

import copy
import inspect
import re
import urllib
import urlparse

from django.core.urlresolvers import NoReverseMatch, resolve, reverse
from django.template import (
    TemplateSyntaxError, Library, VariableDoesNotExist, Node, Variable
)
from django.utils.encoding import smart_str, smart_unicode
from django.utils.text import unescape_string_literal

from common.utils import urlquote

from ..api import object_navigation
from ..classes import Menu
from ..forms import MultiItemForm

register = Library()


@register.assignment_tag(takes_context=True)
def get_top_menu_links(context):
    return Menu.get('main menu').resolve(context=context)


@register.assignment_tag(takes_context=True)
def get_object_facet_links(context):
    return Menu.get('object facet').resolve(context=context)


@register.assignment_tag(takes_context=True)
def get_action_links(context):
    result = []

    for menu_name in ['object menu', 'sidebar menu', 'secondary menu']:
        links = Menu.get(name=menu_name).resolve(context)
        if links:
            result.append(links)

    return result


@register.simple_tag(takes_context=True)
def get_multi_item_links_form(context, object_list):
    first_object = object_list[0]

    actions = []#(link.url, link.text) for link in Menu.get('multi items').resolve(context=context, obj=first_object)]
    form = MultiItemForm(actions=actions)
    context.update({'multi_item_form': form, 'multi_item_actions': actions})
    return ''


@register.assignment_tag(takes_context=True)
def get_object_links(context):
    return Menu.get('object menu').resolve(context=context)

