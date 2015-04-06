from __future__ import unicode_literals

from django.template import Context, Library
from django.template.loader import get_template

register = Library()


@register.assignment_tag(takes_context=True)
def render_subtemplate(context, template_name, template_context):
    """
    Renders the specified template with the mixed parent and
    subtemplate contexts
    """

    new_context = Context(context)
    new_context.update(Context(template_context))
    return get_template(template_name).render(new_context)

