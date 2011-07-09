import re

from django.template import Node, TemplateSyntaxError, Library, Variable

register = Library()


class CopyNode(Node):
    def __init__(self, source_variable, var_name, delete_old=False):
        self.source_variable = source_variable
        self.var_name = var_name
        self.delete_old = delete_old

    def render(self, context):
        context[Variable(self.var_name).resolve(context)] = Variable(self.source_variable).resolve(context)
        if self.delete_old:
            context[Variable(self.source_variable).resolve(context)] = u''
        return ''


@register.tag
def copy_variable(parser, token):
    return parse_tag(parser, token)


@register.tag
def rename_variable(parser, token):
    return parse_tag(parser, token, {'delete_old': True})


def parse_tag(parser, token, *args, **kwargs):
    # This version uses a regular expression to parse tag contents.
    try:
        # Splitting by None == splitting by spaces.
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise TemplateSyntaxError('%r tag requires arguments' % token.contents.split()[0])
    m = re.search(r'(.*?) as ([\'"]*\w+[\'"]*)', arg)
    if not m:
        raise TemplateSyntaxError('%r tag had invalid arguments' % tag_name)
    source_variable, var_name = m.groups()
    return CopyNode(source_variable, var_name, *args, **kwargs)
