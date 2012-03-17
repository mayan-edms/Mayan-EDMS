from __future__ import absolute_import 

import logging

from django.core.urlresolvers import RegexURLResolver, RegexURLPattern, Resolver404, get_resolver

from django.template import (TemplateSyntaxError, Library,
    VariableDoesNotExist, Node, Variable)
from django.utils.text import unescape_string_literal

#__all__ = ('resolve_to_name',)    
logger = logging.getLogger(__name__)


def get_navigation_objects(context):
    object_list = []

    # Try a simple 'object' search first, for lists templates
    try:
        resolved_object = Variable('object').resolve(context)
    except VariableDoesNotExist:
        try:
            object_name_list = Variable('navigation_object_list').resolve(context)
        except VariableDoesNotExist:
            try:
                object_name_list = [{'object': Variable('navigation_object_name').resolve(context)}]
            except VariableDoesNotExist:
                #try:
                #    object_name_list = [{'object': Variable('list_object_variable_name').resolve(context)}]
                #except VariableDoesNotExist:
                return []
                    #object_name_list = [{'object': 'object'}]
                    #logger.debug('none found, falling back to "object"')
                #else:
                #    logger.debug('found: list_object_variable_name')
            else:
                logger.debug('found: navigation_object_name')
        else:
            logger.debug('found: navigation_object_list')
    else:
        logger.debug('found single object')
        return [{'object': resolved_object}]#, 'object_name': 'object'}]

    logger.debug('object_name_list: %s' % object_name_list)

    for object_name in object_name_list:
        try:
            resolved_object = Variable(object_name['object']).resolve(context)
        except VariableDoesNotExist:
            resolved_object = None
        
        object_list.append({'object': resolved_object})#, 'object_name': 'qwe'})

    logger.debug('object_list: %s' % object_list)
    return object_list


def resolve_template_variable(context, name):
    try:
        return unescape_string_literal(name)
    except ValueError:
        #return Variable(name).resolve(context)
        #TODO: Research if should return always as a str
        return str(Variable(name).resolve(context))
    except TypeError:
        return name
        

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


#http://www.djangosnippets.org/snippets/1378/
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
