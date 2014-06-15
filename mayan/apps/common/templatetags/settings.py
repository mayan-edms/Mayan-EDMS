import re

from django.template import Node
from django.template import TemplateSyntaxError, Library
from django.conf import settings

register = Library()


class SettingsNode(Node):
    def __init__(self, format_string, var_name):
        self.format_string = format_string
        self.var_name = var_name

    def render(self, context):
        context[self.var_name] = getattr(settings, self.format_string, '')
        return ''


@register.tag
def get_setting(parser, token):
    # This version uses a regular expression to parse tag contents.
    try:
        # Splitting by None == splitting by spaces.
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise TemplateSyntaxError('%r tag requires arguments' % token.contents.split()[0])
    m = re.search(r'(.*?) as (\w+)', arg)
    if not m:
        raise TemplateSyntaxError('%r tag had invalid arguments' % tag_name)
    format_string, var_name = m.groups()
    if not (format_string[0] == format_string[-1] and format_string[0] in ('"', "'")):
        raise TemplateSyntaxError('%r tag\'s argument should be in quotes' % tag_name)
    return SettingsNode(format_string[1:-1], var_name)
