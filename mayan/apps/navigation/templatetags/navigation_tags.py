from __future__ import absolute_import 

import copy
import re
import urlparse
import urllib

from django.core.urlresolvers import reverse, NoReverseMatch
from django.template import (TemplateSyntaxError, Library,
    VariableDoesNotExist, Node, Variable)
from django.utils.text import unescape_string_literal
from django.utils.translation import ugettext as _
from django.utils.encoding import smart_str, force_unicode, smart_unicode

from common.utils import urlquote

from ..api import (object_navigation, multi_object_navigation,
    top_menu_entries, sidebar_templates)
from ..forms import MultiItemForm
from ..utils import resolve_to_name

register = Library()


class TopMenuNavigationNode(Node):
    def render(self, context):
        request = Variable('request').resolve(context)
        current_path = request.META['PATH_INFO']
        current_view = resolve_to_name(current_path)

        all_menu_links = [entry.get('link', {}) for entry in top_menu_entries]
        menu_links = resolve_links(context, all_menu_links, current_view, current_path)

        for index, link in enumerate(top_menu_entries):
            if current_view in link.get('children_views', []):
                menu_links[index]['active'] = True

            for child_path_regex in link.get('children_path_regex', []):
                if re.compile(child_path_regex).match(current_path.lstrip('/')):
                    menu_links[index]['active'] = True
            
            for children_view_regex in link.get('children_view_regex', []):
                if re.compile(children_view_regex).match(current_view):
                    menu_links[index]['active'] = True

        context['menu_links'] = menu_links
        return ''


@register.tag
def get_top_menu_links(parser, token):
    return TopMenuNavigationNode()


def resolve_arguments(context, src_args):
    args = []
    kwargs = {}
    if type(src_args) == type([]):
        for i in src_args:
            val = resolve_template_variable(context, i)
            if val:
                args.append(val)
    elif type(src_args) == type({}):
        for key, value in src_args.items():
            val = resolve_template_variable(context, value)
            if val:
                kwargs[key] = val
    else:
        val = resolve_template_variable(context, src_args)
        if val:
            args.append(val)

    return args, kwargs


def resolve_links(context, links, current_view, current_path, parsed_query_string=None):
    """
    Express a list of links from definition to final values
    """
    context_links = []
    for link in links:
        # Check to see if link has conditional display
        if 'condition' in link:
            condition_result = link['condition'](context)
        else:
            condition_result = True

        if condition_result:
            new_link = copy.copy(link)
            try:
                args, kwargs = resolve_arguments(context, link.get('args', {}))
            except VariableDoesNotExist:
                args = []
                kwargs = {}

            if 'view' in link:
                if not link.get('dont_mark_active', False):
                    new_link['active'] = link['view'] == current_view

                try:
                    if kwargs:
                        new_link['url'] = reverse(link['view'], kwargs=kwargs)
                    else:
                        new_link['url'] = reverse(link['view'], args=args)
                        if link.get('keep_query', False):
                            new_link['url'] = urlquote(new_link['url'], parsed_query_string)
                except NoReverseMatch, err:
                    new_link['url'] = '#'
                    new_link['error'] = err
            elif 'url' in link:
                if not link.get('dont_mark_active', False):
                    new_link['active'] = link['url'] == current_path

                if kwargs:
                    new_link['url'] = link['url'] % kwargs
                else:
                    new_link['url'] = link['url'] % args
                    if link.get('keep_query', False):
                        new_link['url'] = urlquote(new_link['url'], parsed_query_string)
            else:
                new_link['active'] = False

            if 'conditional_highlight' in link:
                new_link['active'] = link['conditional_highlight'](context)

            if 'conditional_disable' in link:
                new_link['disabled'] = link['conditional_disable'](context)
            else:
                new_link['disabled'] = False

            if current_view in link.get('children_views', []):
                new_link['active'] = True

            for child_url_regex in link.get('children_url_regex', []):
                if re.compile(child_url_regex).match(current_path.lstrip('/')):
                    new_link['active'] = True

            for children_view_regex in link.get('children_view_regex', []):
                if re.compile(children_view_regex).match(current_view):
                    new_link['active'] = True

            for cls in link.get('children_classes', []):
                obj, object_name = get_navigation_object(context)
                if type(obj) == cls or obj == cls:
                    new_link['active'] = True

            context_links.append(new_link)
    return context_links


def get_navigation_object(context):
    try:
        object_name = Variable('navigation_object_name').resolve(context)
    except VariableDoesNotExist:
        object_name = 'object'

    try:
        obj = Variable(object_name).resolve(context)
    except VariableDoesNotExist:
        obj = None

    return obj, object_name


def _get_object_navigation_links(context, menu_name=None, links_dict=object_navigation):
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
        navigation_object_links = Variable('overrided_object_links').resolve(context)
        if navigation_object_links:
            return [link for link in resolve_links(context, navigation_object_links, current_view, current_path, parsed_query_string)]
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
        for link in resolve_links(context, links, current_view, current_path, parsed_query_string):
            context_links.append(link)
    except KeyError:
        pass

    obj, object_name = get_navigation_object(context)

    try:
        links = links_dict[menu_name][type(obj)]['links']
        for link in resolve_links(context, links, current_view, current_path, parsed_query_string):
            context_links.append(link)
    except KeyError:
        pass

    return context_links


def resolve_template_variable(context, name):
    try:
        return unescape_string_literal(name)
    except ValueError:
        #return Variable(name).resolve(context)
        #TODO: Research if should return always as a str
        return str(Variable(name).resolve(context))
    except TypeError:
        return name


class GetNavigationLinks(Node):
    def __init__(self, menu_name=None, links_dict=object_navigation, var_name='object_navigation_links'):
        self.menu_name = menu_name
        self.links_dict = links_dict
        self.var_name = var_name

    def render(self, context):
        menu_name = resolve_template_variable(context, self.menu_name)
        context[self.var_name] = _get_object_navigation_links(context, menu_name, links_dict=self.links_dict)
        obj, object_name = get_navigation_object(context)
        context['navigation_object'] = obj
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
    new_context.update({
        'horizontal': True,
        'object_navigation_links': _get_object_navigation_links(context)    
    })
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
        'form': MultiItemForm(actions=[(link['url'], link['text']) for link in _get_object_navigation_links(context, links_dict=multi_object_navigation)]),
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
