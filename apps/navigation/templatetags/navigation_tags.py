import copy
import re

from django.core.urlresolvers import reverse, NoReverseMatch
from django.template import TemplateSyntaxError, Library, \
                            VariableDoesNotExist, Node, Variable
from django.utils.text import unescape_string_literal
from django.utils.translation import ugettext as _

from django.template import Context

from navigation.api import object_navigation, multi_object_navigation, \
    menu_links as menu_navigation, sidebar_templates
from navigation.forms import MultiItemForm
from navigation.utils import resolve_to_name

register = Library()


def process_links(links, view_name, url):
    items = []
    active_item = None
    for item, count in zip(links, range(len(links))):
        item_view = 'view' in item and item['view']
        item_url = 'url' in item and item['url']
        new_link = item.copy()
        if view_name == item_view or url == item_url:
            new_link['active'] = True
            active_item = item
        else:
            new_link['active'] = False
            if 'links' in item:
                for child_link in item['links']:
                    child_view = 'view' in child_link and child_link['view']
                    child_url = 'url' in child_link and child_link['url']
                    if view_name == child_view or url == child_url:
                        active_item = item
        new_link.update({
            'first': count == 0,
            'url': item_view and reverse(item_view) or item_url or u'#',
            })
        items.append(new_link)

    return items, active_item


class NavigationNode(Node):
    def __init__(self, navigation, *args, **kwargs):
        self.navigation = navigation

    def render(self, context):
        request = Variable('request').resolve(context)
        view_name = resolve_to_name(request.META['PATH_INFO'])

        main_items, active_item = process_links(links=self.navigation, view_name=view_name, url=request.META['PATH_INFO'])
        context['navigation_main_links'] = main_items
        if active_item and 'links' in active_item:
            secondary_links, active_item = process_links(links=active_item['links'], view_name=view_name, url=request.META['PATH_INFO'])
            context['navigation_secondary_links'] = secondary_links
        return ''


@register.tag
def main_navigation(parser, token):
    #args = token.split_contents()

#    if len(args) != 3 or args[1] != 'as':
#        raise TemplateSyntaxError("'get_all_states' requires 'as variable' (got %r)" % args)

    #return NavigationNode(variable=args[2], navigation=navigation)
    return NavigationNode(navigation=menu_navigation)


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


def resolve_links(context, links, current_view, current_path):
    context_links = []
    for link in links:
        new_link = copy.copy(link)
        try:
            args, kwargs = resolve_arguments(context, link.get('args', {}))
        except VariableDoesNotExist:
            args = []
            kwargs = {}

        if 'view' in link:
            new_link['active'] = link['view'] == current_view

            try:
                if kwargs:
                    new_link['url'] = reverse(link['view'], kwargs=kwargs)
                else:
                    new_link['url'] = reverse(link['view'], args=args)
            except NoReverseMatch, err:
                new_link['url'] = '#'
                new_link['error'] = err
        elif 'url' in link:
            new_link['active'] = link['url'] == current_path
            if kwargs:
                new_link['url'] = link['url'] % kwargs
            else:
                new_link['url'] = link['url'] % args
        else:
            new_link['active'] = False
        context_links.append(new_link)
    return context_links


def _get_object_navigation_links(context, menu_name=None, links_dict=object_navigation):
    current_path = Variable('request').resolve(context).META['PATH_INFO']
    current_view = resolve_to_name(current_path)
    context_links = []

    try:
        """
        Override the navigation links dictionary with the provided
        link list
        """
        navigation_object_links = Variable('navigation_object_links').resolve(context)
        if navigation_object_links:
            return [link for link in resolve_links(context, navigation_object_links, current_view, current_path)]
    except VariableDoesNotExist:
        pass

    try:
        object_name = Variable('navigation_object_name').resolve(context)
    except VariableDoesNotExist:
        object_name = 'object'

    try:
        obj = Variable(object_name).resolve(context)
    except VariableDoesNotExist:
        obj = None

    try:
        links = links_dict[menu_name][current_view]['links']
        for link in resolve_links(context, links, current_view, current_path):
            context_links.append(link)
    except KeyError:
        pass

    try:
        links = links_dict[menu_name][type(obj)]['links']
        for link in resolve_links(context, links, current_view, current_path):
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
    return {
        'request': context['request'],
        'horizontal': True,
        'object_navigation_links': _get_object_navigation_links(context)
    }


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


class EvaluateLinkNone(Node):
    def __init__(self, condition, var_name):
        self.condition = condition
        self.var_name = var_name

    def render(self, context):
        condition = Variable(self.condition).resolve(context)
        if condition:
            context[self.var_name] = condition(Context(context))
            return u''
        else:
            context[self.var_name] = True
            return u''


@register.tag
def evaluate_link(parser, token):
    tag_name, arg = token.contents.split(None, 1)
    m = re.search(r'("?\w+"?)?.?as (\w+)', arg)
    if not m:
        raise TemplateSyntaxError("%r tag had invalid arguments" % tag_name)

    condition, var_name = m.groups()
    return EvaluateLinkNone(condition=condition, var_name=var_name)
