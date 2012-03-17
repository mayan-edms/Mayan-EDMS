from __future__ import absolute_import 

import copy
import re
import urlparse
import urllib
import logging

from django.core.urlresolvers import reverse, NoReverseMatch
from django.template import (TemplateSyntaxError, Library,
    VariableDoesNotExist, Node, Variable)
from django.utils.translation import ugettext as _
from django.utils.encoding import smart_str, force_unicode, smart_unicode

from common.utils import urlquote

from ..api import (object_navigation, multi_object_navigation,
    top_menu_entries, sidebar_templates, get_context_object_navigation_links)
from ..forms import MultiItemForm
from ..utils import (resolve_to_name, resolve_arguments, resolve_template_variable,
    get_navigation_objects)
from .. import main_menu

register = Library()
logger = logging.getLogger(__name__)


class TopMenuNavigationNode(Node):
    def render(self, context):
        #request = Variable('request').resolve(context)
        #current_path = request.META['PATH_INFO']
        #current_view = resolve_to_name(current_path)
            
        #all_menu_links = []#[entry.get('link', {}) for entry in top_menu_entries]
        #menu_links = resolve_links(context, all_menu_links, current_view, current_path)

        #for index, link in enumerate(top_menu_entries):
        #    #if current_view in link.get('children_views', []):
        #    #    menu_links[index]['active'] = True
        #    #for child_path_regex in link.get('children_path_regex', []):
        #    #    if re.compile(child_path_regex).match(current_path.lstrip('/')):
        #    #        menu_links[index]['active'] = True
        #    #for children_view_regex in link.get('children_view_regex', []):
        #    #    if re.compile(children_view_regex).match(current_view):
        #    #        menu_links[index]['active'] = True
        #    pass
        #context['menu_links'] = []#menu_links
        context['menu_links'] = [menu.get('link').resolve(context) for menu in main_menu.getchildren()]
        return ''


@register.tag
def get_top_menu_links(parser, token):
    return TopMenuNavigationNode()


class GetNavigationLinks(Node):
    def __init__(self, menu_name=None, links_dict=object_navigation, var_name='object_navigation_links'):
        self.menu_name = menu_name
        self.links_dict = links_dict
        self.var_name = var_name

    def render(self, context):
        menu_name = resolve_template_variable(context, self.menu_name)
        context[self.var_name] = get_context_object_navigation_links(context, menu_name, links_dict=self.links_dict)
        object_list = get_navigation_objects(context)
        if object_list:
            context['navigation_object'] = object_list[0]['object']
        return ''


@register.tag
def get_object_navigation_links(parser, token):
    tag_name, arg = token.contents.split(None, 1)

    m = re.search(r'("?\w+"?)?.?as (\w+)', arg)
    if not m:
        raise TemplateSyntaxError("%r tag had invalid arguments" % tag_name)

    menu_name, var_name = m.groups()
    return GetNavigationLinks(menu_name=menu_name, var_name=var_name)


@register.inclusion_tag('generic_navigation.html', takes_context=True)
def object_navigation_template(context):
    new_context = copy.copy(context)
    #new_context.update({
    #    'horizontal': True,
    #    'object_navigation_links': get_object_navigation_links(context)    
    #})
    return new_context
    
    
@register.tag
def get_multi_item_links(parser, token):
    tag_name, arg = token.contents.split(None, 1)
    m = re.search(r'("?\w+"?)?.?as (\w+)', arg)
    if not m:
        raise TemplateSyntaxError("%r tag had invalid arguments" % tag_name)

    menu_name, var_name = m.groups()
    return GetNavigationLinks(menu_name=menu_name, links_dict=multi_object_navigation, var_name=var_name)


@register.inclusion_tag('generic_form_instance.html', takes_context=True)
def get_multi_item_links_form(context):
    new_context = copy.copy(context)
    new_context.update({
        'form': MultiItemForm(actions=[(link['url'], link['text']) for link in get_context_object_navigation_links(context, links_dict=multi_object_navigation)]),
        'title': _(u'Selected item actions:'),
        'form_action': reverse('multi_object_action_view'),
        'submit_method': 'get',
    })
    return new_context


class GetSidebarTemplatesNone(Node):
    def __init__(self, var_name='sidebar_templates'):
        self.var_name = var_name

    def render(self, context):
        request = Variable('request').resolve(context)
        view_name = resolve_to_name(request.META['PATH_INFO'])
        context[self.var_name] = sidebar_templates.get(view_name, [])
        return ''


@register.tag
def get_sidebar_templates(parser, token):
    tag_name, arg = token.contents.split(None, 1)

    m = re.search(r'("?\w+"?)?.?as (\w+)', arg)
    if not m:
        raise TemplateSyntaxError("%r tag had invalid arguments" % tag_name)

    menu_name, var_name = m.groups()
    return GetSidebarTemplatesNone(var_name=var_name)
