import types

from django.conf import settings
from django.core.urlresolvers import reverse, NoReverseMatch
from django.core.urlresolvers import RegexURLResolver, RegexURLPattern, Resolver404, get_resolver
from django.template import TemplateSyntaxError, Library, \
                            VariableDoesNotExist, Node, Variable
from django.utils.text import unescape_string_literal

#from common.api import object_navigation
from web_theme.conf import settings as web_theme_settings

register = Library()


class GetThemeNode(Node):
    def __init__(self, var_name, *args):
        self.var_name = var_name

    def render(self, context):
        context['web_theme'] = web_theme_settings.THEME
        return ''


import re

@register.tag
def get_theme(parser, token):
    try:
        # Splitting by None == splitting by spaces.
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires arguments" % token.contents.split()[0]

    #m = re.search(r'(.*?) as (\w+)', arg)
    m = re.search(r'as (\w+)', arg)
    if not m:
        raise template.TemplateSyntaxError, "%r tag had invalid arguments" % tag_name
    #format_string, var_name = m.groups()
    var_name = m.groups()
    
    #if not (format_string[0] == format_string[-1] and format_string[0] in ('"', "'")):
    #    raise template.TemplateSyntaxError, "%r tag's argument should be in quotes" % tag_name
    return GetThemeNode(var_name)    
