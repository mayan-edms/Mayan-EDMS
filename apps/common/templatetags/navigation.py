import types
import copy 

from django.conf import settings
from django.core.urlresolvers import reverse, NoReverseMatch
from django.core.urlresolvers import RegexURLResolver, RegexURLPattern, Resolver404, get_resolver
from django.template import TemplateSyntaxError, Library, \
                            VariableDoesNotExist, Node, Variable
from django.utils.text import unescape_string_literal

from common.api import object_navigation, menu_links as menu_navigation

register = Library()


def process_links(links, view_name, url):
    items = []
    active_item = None
    for item, count in zip(links, range(len(links))):
        item_view = 'view' in item and item['view']
        item_url = 'url' in item and item['url']
        if view_name == item_view or url == item_url:
            active = True
            active_item = item
        else:
            active = False
            if 'links' in item:
                for child_link in item['links']:
                    child_view = 'view' in child_link and child_link['view']
                    child_url = 'url' in child_link and child_link['url']
                    if view_name == child_view or url == child_url:
                        active = True
                        active_item = item                
            
        items.append(
            {
                'first':count==0,
                'active':active,
                'url':item_view and reverse(item_view) or item_url or '#',
                'text':unicode(item['text']),
                'famfam':'famfam' in item and item['famfam'],
            }
        )
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
    args = token.split_contents()

#    if len(args) != 3 or args[1] != 'as':
#        raise TemplateSyntaxError("'get_all_states' requires 'as variable' (got %r)" % args)

    #return NavigationNode(variable=args[2], navigation=navigation)    
    return NavigationNode(navigation=menu_navigation)    


#http://www.djangosnippets.org/snippets/1378/
__all__ = ('resolve_to_name',)

def _pattern_resolve_to_name(self, path):
    match = self.regex.search(path)
    if match:
        name = ""
        if self.name:
            name = self.name
        elif hasattr(self, '_callback_str'):
            name = self._callback_str
        else:
            name = "%s.%s" % (self.callback.__module__, self.callback.func_name)
        return name

def _resolver_resolve_to_name(self, path):
    tried = []
    match = self.regex.search(path)
    if match:
        new_path = path[match.end():]
        for pattern in self.url_patterns:
            try:
                name = pattern.resolve_to_name(new_path)
            except Resolver404, e:
                tried.extend([(pattern.regex.pattern + '   ' + t) for t in e.args[0]['tried']])
            else:
                if name:
                    return name
                tried.append(pattern.regex.pattern)
        raise Resolver404, {'tried': tried, 'path': new_path}


# here goes monkeypatching
RegexURLPattern.resolve_to_name = _pattern_resolve_to_name
RegexURLResolver.resolve_to_name = _resolver_resolve_to_name

def resolve_to_name(path, urlconf=None):
    return get_resolver(urlconf).resolve_to_name(path)

@register.filter
def resolve_url_name(value):
    return resolve_to_name(value)

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
        args, kwargs = resolve_arguments(context, link.get('args', {}))
        
        if 'view' in link:
            new_link['active'] = link['view'] == current_view
            args, kwargs = resolve_arguments(context, link.get('args', {}))
                
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

def _get_object_navigation_links(context, menu_name=None):
    current_path = Variable('request').resolve(context).META['PATH_INFO']
    current_view = resolve_to_name(current_path)#.get_full_path())
    context_links = []    

    try:
        object_name = Variable('navigation_object_name').resolve(context)
    except VariableDoesNotExist:
        object_name = 'object'
        
    try:
        obj = Variable(object_name).resolve(context)
    except VariableDoesNotExist:
        obj = None
        
    try:
        links = object_navigation[menu_name][current_view]['links']
        for link in resolve_links(context, links, current_view, current_path):
            context_links.append(link)
    except KeyError:
        pass

    try:
        links = object_navigation[menu_name][type(obj)]['links']
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
    def __init__(self, *args):
        self.menu_name = None
        if args:
            self.menu_name = args[0]

    def render(self, context):
        menu_name = resolve_template_variable(context, self.menu_name)
        context['object_navigation_links'] = _get_object_navigation_links(context, menu_name)
        return ''


@register.tag
def get_object_navigation_links(parser, token):
    args = token.split_contents()
    return GetNavigationLinks(*args[1:])
    
    
def object_navigation_template(context):
    return {
        'request':context['request'],
        'horizontal':True,
        'object_navigation_links':_get_object_navigation_links(context)
    }
    return new_context
register.inclusion_tag('generic_navigation.html', takes_context=True)(object_navigation_template)
 
