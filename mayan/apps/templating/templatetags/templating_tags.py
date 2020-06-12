from django.template import Library

register = Library()


@register.simple_tag(takes_context=True)
def set(context, name, value):
    """
    Set a context variable to a specific value.
    """
    context[name] = value
    return ''
