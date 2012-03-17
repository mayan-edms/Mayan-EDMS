from __future__ import absolute_import 

import urlparse
import urllib
import logging
import re

from django.template import (TemplateSyntaxError, Library,
    VariableDoesNotExist, Node, Variable)
from django.utils.encoding import smart_str, force_unicode, smart_unicode
from django.core.urlresolvers import reverse, NoReverseMatch
from django.utils.http import urlquote
from django.utils.http import urlencode

from elementtree.ElementTree import Element, SubElement

#from common.utils import urlquote

from .utils import (resolve_to_name, resolve_arguments,
    resolve_template_variable, get_navigation_objects)
from . import main_menu

object_navigation = {}
multi_object_navigation = {}
model_list_columns = {}
sidebar_templates = {}
top_menu_entries = []

link_binding = {}

logger = logging.getLogger(__name__)


class ResolvedLink(object):
    active = False
   
    
class Link(object):
    def __init__(self, text, view, klass=None, args=None, sprite=None,
        icon=None, permissions=None, condition=None, conditional_disable=None,
        description=None, dont_mark_active=False, children_view_regex=None,
        keep_query=False, children_classes=None, children_url_regex=None,
        children_views=None, conditional_highlight=None):
            
        self.text = text
        self.view = view
        self.args = args or {}
        #self.kwargs = kwargs or {}
        self.sprite = sprite
        self.icon = icon
        self.permissions = permissions or []
        self.condition = condition
        self.conditional_disable = conditional_disable
        self.description = description
        self.dont_mark_active = dont_mark_active
        self.children_view_regex = children_view_regex or []
        self.klass = klass
        self.keep_query = keep_query
        self.conditional_highlight = conditional_highlight  # Used by dynamic sources
        self.children_views = children_views or []
        self.children_classes = children_classes or []

    def resolve(self, context):
        request = Variable('request').resolve(context)
        current_path = request.META['PATH_INFO']
        current_view = resolve_to_name(current_path)
        
        # Preserve unicode data in URL query
        previous_path = smart_unicode(urllib.unquote_plus(smart_str(request.get_full_path()) or smart_str(request.META.get('HTTP_REFERER', u'/'))))
        query_string = urlparse.urlparse(previous_path).query
        parsed_query_string = urlparse.parse_qs(query_string)
            
        # Check to see if link has conditional display
        if self.condition:
            condition_result = self.condition(context)
        else:
            condition_result = True

        if condition_result:
            resolved_link = ResolvedLink()
            resolved_link.text = self.text
            resolved_link.sprite = self.sprite
            resolved_link.icon = self.icon
            resolved_link.permissions = self.permissions
            
            try:
                #args, kwargs = resolve_arguments(context, self.get('args', {}))
                args, kwargs = resolve_arguments(context, self.args)
            except VariableDoesNotExist:
                args = []
                kwargs = {}

            if self.view:
                if not self.dont_mark_active:
                    #new_link['active'] = link['view'] == current_view
                    resolved_link.active = self.view == current_view

                try:
                    if kwargs:
                        resolved_link.url = reverse(self.view, kwargs=kwargs)
                    else:
                        resolved_link.url = reverse(self.view, args=args)
                        if self.keep_query:
                            resolved_link.url = u'%s?%s' % (urlquote(resolved_link.url), urlencode(parsed_query_string, doseq=True))  

                except NoReverseMatch, exc:
                    resolved_link.url = '#'
                    resolved_link.error = exc
            elif self.url:
                if not self.dont_mark_active:
                    #new_link['active'] = link['url'] == current_path
                    resolved_link.url.active = self.url == current_path
                    
                if kwargs:
                    #new_link['url'] = link['url'] % kwargs
                    resolved_link.url = self.url % kwargs
                else:
                    #new_link['url'] = link['url'] % args
                    resolved_link.url = self.url % args
                    if link.keep_query:
                        #new_link['url'] = urlquote(new_link['url'], parsed_query_string)
                        resolved_link.url = urlquote(resolved_link.url, parsed_query_string)
            else:
                #new_link['active'] = False
                resolved_link.active = False

            if self.conditional_highlight:
                #new_link['active'] = link['conditional_highlight'](context)
                resolved_link.active = self.conditional_highlight(context)

            if self.conditional_disable:
                #new_link['disabled'] = link['conditional_disable'](context)
                resolved_link.disabled = self.conditional_disable(context)
            else:
                #new_link['disabled'] = False
                resolved_link.disabled = False

            if current_view in self.children_views:
                #new_link['active'] = True
                resolved_link.active = True

            #for child_url_regex in link.get('children_url_regex', []):
            #    if re.compile(child_url_regex).match(current_path.lstrip('/')):
            #        #new_link['active'] = True
            #        resolved_link.active = True

            for children_view_regex in self.children_view_regex:
                if re.compile(children_view_regex).match(current_view):
                    resolved_link.active = True

            for cls in self.children_classes:
                object_list = get_navigation_objects(context)
                if object_list:
                    if type(object_list[0]['object']) == cls or object_list[0]['object'] == cls:
                        #new_link['active'] = True
                        resolved_link.active = True

            return resolved_link
            #context_links.append(new_link)


def bind_links(sources, links, menu_name=None, position=0):
    """
    Associate a link to a model, a view, or an url
    """
    link_binding.setdefault(menu_name, {})
    for source in sources:
        link_binding[menu_name].setdefault(source, {'links': []})
        link_binding[menu_name][source]['links'].extend(links)


def register_top_menu(name, link, position=None):
    """
    Register a new menu entry for the main menu displayed at the top
    of the page
    """
    new_menu = SubElement(main_menu, name, link=link, position=position)
    
    sorted_menus = sorted(main_menu.getchildren(), key=lambda k: (k.get('position') < 0, k.get('position')))
    main_menu.clear()

    for menu in sorted_menus:
        main_menu.append(menu)
        
    return new_menu


def register_model_list_columns(model, columns):
    """
    Define which columns will be displayed in the generic list template
    for a given model
    """

    model_list_columns.setdefault(model, [])
    model_list_columns[model].extend(columns)


def register_sidebar_template(source_list, template_name):
    for source in source_list:
        sidebar_templates.setdefault(source, [])
        sidebar_templates[source].append(template_name)


# TODO
def register_multi_item_links(src, links, menu_name=None):
    """
    Register a multiple item action action to be displayed in the
    generic list template
    """
    # TODO: simplify by removing __iter__ support
    multi_object_navigation.setdefault(menu_name, {})
    if hasattr(src, '__iter__'):
        for one_src in src:
            multi_object_navigation[menu_name].setdefault(one_src, {'links': []})
            multi_object_navigation[menu_name][one_src]['links'].extend(links)
    else:
        multi_object_navigation[menu_name].setdefault(src, {'links': []})
        multi_object_navigation[menu_name][src]['links'].extend(links)


def get_context_object_navigation_links(context, menu_name=None, links_dict=link_binding):
    request = Variable('request').resolve(context)
    current_path = request.META['PATH_INFO']
    current_view = resolve_to_name(current_path)
    context_links = []

    # Don't fudge with the original global dictionary
    links_dict = links_dict.copy()

    # Preserve unicode data in URL query
    #previous_path = smart_unicode(urllib.unquote_plus(smart_str(request.get_full_path()) or smart_str(request.META.get('HTTP_REFERER', u'/'))))
    #query_string = urlparse.urlparse(previous_path).query
    #parsed_query_string = urlparse.parse_qs(query_string)

    try:
        """
        Override the navigation links dictionary with the provided
        link list
        """
        navigation_object_links = Variable('overrided_object_links').resolve(context)
        if navigation_object_links:
            return [link.resolve(context) for link in navigation_object_links]
    except VariableDoesNotExist:
        pass

    # TODO: who uses this?  Remove if no one.
    try:
        """
        Check for and inject a temporary navigation dictionary
        """
        temp_navigation_links = Variable('temporary_navigation_links').resolve(context)
        if temp_navigation_links:
            links_dict.update(temp_navigation_links)
    except VariableDoesNotExist:
        pass

    try:
        for link in links_dict[menu_name][current_view]['links']:
            context_links.append(link.resolve(context))
    except KeyError:
        pass

    for resolved_object in get_navigation_objects(context):
        try:
            for link in links_dict[menu_name][type(resolved_object['object'])]['links']:
                context_links.append(link.resolve(context))
        except KeyError:
            pass

    return context_links
