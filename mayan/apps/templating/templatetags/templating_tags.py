from django.template import Library

register = Library()


@register.simple_tag(takes_context=True)
def templating_set(context, name, value):
    context[name] = value
    return ''
