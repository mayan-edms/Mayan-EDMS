import re

from django.template import (Node, TemplateSyntaxError, Library,
    Variable, Context)
from django.template.loader import get_template

from common.utils import return_attrib

register = Library()


class RenderSubtemplateNode(Node):
    def __init__(self, template_name, template_context, var_name):
        self.template_name = template_name
        self.template_context = template_context
        self.var_name = var_name

    def render(self, context):
        template_name = Variable(self.template_name).resolve(context)
        template_context = Variable(self.template_context).resolve(context)

        new_context = Context(context)
        new_context.update(Context(template_context, autoescape=context.autoescape))

        csrf_token = context.get('csrf_token', None)
        if csrf_token is not None:
            new_context['csrf_token'] = csrf_token

        context[self.var_name] = get_template(template_name).render(new_context)
        return ''


@register.tag
def render_subtemplate(parser, token):
    # This version uses a regular expression to parse tag contents.
    try:
        # Splitting by None == splitting by spaces.
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise TemplateSyntaxError('%r tag requires arguments' % token.contents.split()[0])
    m = re.search(r'(.*?) (.*?) as (\w+)', arg)
    if not m:
        raise TemplateSyntaxError('%r tag had invalid arguments' % tag_name)
    template_name, template_context, var_name = m.groups()

    if (template_name[0] == template_name[-1] and template_name[0] in ('"', "'")):
        raise TemplateSyntaxError('%r tag\'s template name argument should not be in quotes' % tag_name)

    if (template_context[0] == template_context[-1] and template_context[0] in ('"', "'")):
        raise TemplateSyntaxError('%r tag\'s template context argument should not be in quotes' % tag_name)

    return RenderSubtemplateNode(template_name, template_context, var_name)
    #format_string[1:-1]


@register.simple_tag(takes_context=True)
def get_object_list_object_name(context, source_object):
    object_list_object_name = context.get('object_list_object_name')
    if object_list_object_name:
        context['object'] = return_attrib(source_object, object_list_object_name)
    else:
        context['object'] = source_object
    
    return ''
        
