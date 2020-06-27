from django.template import Library

register = Library()


@register.filter
def dict_get(dictionary, key):
    """
    Return the value for the given key or '' if not found.
    """
    return dictionary.get(key, '')


@register.simple_tag(takes_context=True)
def set(context, name, value):
    """
    Set a context variable to a specific value.
    """
    context[name] = value
    return ''


@register.filter
def split(obj, separator):
    """
    Return a list of the words in the string, using sep as the delimiter string.
    """
    return obj.split(separator)
