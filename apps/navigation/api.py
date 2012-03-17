from __future__ import absolute_import 

import urlparse
import urllib
import logging

from django.template import (TemplateSyntaxError, Library,
    VariableDoesNotExist, Node, Variable)
from django.utils.encoding import smart_str, force_unicode, smart_unicode
from django.core.urlresolvers import reverse, NoReverseMatch

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
    def __init__(self, text, view, klass=None, args=None, sprite=None, icon=None, permissions=None, condition=None, conditional_disable=None, description=None, dont_mark_active=False, children_view_regex=None, keep_query=False):
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
        self.children_view_regex = children_view_regex
        self.klass = klass
        self.keep_query = keep_query
        
        #
        self.conditional_highlight = None
        self.children_views = []
        self.children_classes = []

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
            #new_link = {}#copy.copy(link)
            resolved_link = ResolvedLink()
            resolved_link.text = self.text
            resolved_link.sprite = self.sprite
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
                        #new_link['url'] = reverse(link['view'], kwargs=kwargs)
                        resolved_link.url = reverse(self.view, kwargs=kwargs)
                    else:
#                        new_link['url'] = reverse(link['view'], args=args)
                        resolved_link.url = reverse(self.view, args=args)
                        if self.keep_query:
                            #print 'parsed_query_string', parsed_query_string
                            #new_link['url'] = urlquote(new_link['url'], parsed_query_string)
                            resolved_link.url = urlquote(resolved_link.url, parsed_query_string)
                except NoReverseMatch, exc:
                    #new_link['url'] = '#'
                    resolved_link.url = '#'
                    #new_link['error'] = err
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

            #for children_view_regex in link.get('children_view_regex', []):
            #    if re.compile(children_view_regex).match(current_view):
            #        #new_link['active'] = True
            #        resolved_link.active = True

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


def register_multi_item_links(src, links, menu_name=None):
    """
    Register a multiple item action action to be displayed in the
    generic list template
    """

    multi_object_navigation.setdefault(menu_name, {})
    if hasattr(src, '__iter__'):
        for one_src in src:
            multi_object_navigation[menu_name].setdefault(one_src, {'links': []})
            multi_object_navigation[menu_name][one_src]['links'].extend(links)
    else:
        multi_object_navigation[menu_name].setdefault(src, {'links': []})
        multi_object_navigation[menu_name][src]['links'].extend(links)


def register_top_menu(name, link, children_views=None, children_path_regex=None, children_view_regex=None, position=None):
    """
    Register a new menu entry for the main menu displayed at the top
    of the page
    """
    menu = SubElement(main_menu, name, link=link)
    #entry = {'link': link, 'name': name}
    #if children_views:
    #    entry['children_views'] = children_views
    #if children_path_regex:
    #    entry['children_path_regex'] = children_path_regex
    #if children_view_regex:
    #    entry['children_view_regex'] = children_view_regex
    #if position is not None:
    #    entry['position'] = position
    #    top_menu_entries.insert(position, entry)
    #else:
    #    length = len(top_menu_entries)
    #    entry['position'] = length
    #    top_menu_entries.append(entry)

    #sort_menu_entries()
    # 
    #return entry
    return menu


#def sort_menu_entries():
#    global top_menu_entries
#    top_menu_entries = sorted(top_menu_entries, key=lambda k: (k['position'] < 0, k['position']))


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


def get_context_object_navigation_links(context, menu_name=None, links_dict=object_navigation):
    request = Variable('request').resolve(context)
    current_path = request.META['PATH_INFO']
    current_view = resolve_to_name(current_path)
    context_links = []

    # Don't fudge with the original global dictionary
    links_dict = links_dict.copy()

    # Preserve unicode data in URL query
    previous_path = smart_unicode(urllib.unquote_plus(smart_str(request.get_full_path()) or smart_str(request.META.get('HTTP_REFERER', u'/'))))
    query_string = urlparse.urlparse(previous_path).query
    parsed_query_string = urlparse.parse_qs(query_string)

    try:
        """
        Override the navigation links dictionary with the provided
        link list
        """
        #navigation_object_links = Variable('overrided_object_links').resolve(context)
        return Variable('overrided_object_links').resolve(context)
        #if navigation_object_links:
        #    return [link for link in resolve_links(context, navigation_object_links, current_view, current_path, parsed_query_string)]
    except VariableDoesNotExist:
        pass

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
        links = links_dict[menu_name][current_view]['links']
        #for link in resolve_links(context, links, current_view, current_path, parsed_query_string):
        #    context_links.append(link)
        context_links.extend(links)
    except KeyError:
        pass

    for resolved_object in get_navigation_objects(context):
        try:
            links = links_dict[menu_name][type(resolved_object['object'])]['links']
            #for link in resolve_links(context, links, current_view, current_path, parsed_query_string):
            #    context_links.append(link)
            context_links.extend(links)
        except KeyError:
            pass

    return context_links
