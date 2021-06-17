import re

from django.template import Library, Node, TemplateSyntaxError

register = Library()


def process_regex_flags(**kwargs):
    result = 0

    REGEX_FLAGS = {
        'ascii': re.ASCII,
        'ignorecase': re.IGNORECASE,
        'locale': re.LOCALE,
        'multiline': re.MULTILINE,
        'dotall': re.DOTALL,
        'verbose': re.VERBOSE
    }

    for key, value in kwargs.items():
        if value is True:
            try:
                result = result | REGEX_FLAGS[key]
            except KeyError:
                raise TemplateSyntaxError(
                    'Unknown or unsupported regular expression '
                    'flag: "{}"'.format(key)
                )

    return result


@register.filter
def dict_get(dictionary, key):
    """
    Return the value for the given key or '' if not found.
    """
    return dictionary.get(key, '')


@register.simple_tag
def method(obj, method, **kwargs):
    """
    Call an object method. {% method object method **kwargs %}
    """
    try:
        return getattr(obj, method)(**kwargs)
    except Exception as exception:
        raise TemplateSyntaxError(
            'Error calling object method; {}'.format(exception)
        )


@register.simple_tag
def regex_findall(pattern, string, **kwargs):
    """
    Return all non-overlapping matches of pattern in string, as a list of
    strings. {% regex_findall pattern string flags %}
    """
    flags = process_regex_flags(**kwargs)
    return re.findall(pattern=pattern, string=string, flags=flags)


@register.simple_tag
def regex_match(pattern, string, **kwargs):
    """
    If zero or more characters at the beginning of string match the regular
    expression pattern, return a corresponding match object.
    {% regex_match pattern string flags %}
    """
    flags = process_regex_flags(**kwargs)
    return re.match(pattern=pattern, string=string, flags=flags)


@register.simple_tag
def regex_search(pattern, string, **kwargs):
    """
    Scan through string looking for the first location where the regular
    expression pattern produces a match, and return a corresponding
    match object. {% regex_search pattern string flags %}
    """
    flags = process_regex_flags(**kwargs)
    return re.search(pattern=pattern, string=string, flags=flags)


@register.simple_tag
def regex_sub(pattern, repl, string, count=0, **kwargs):
    """
    Replacing the leftmost non-overlapping occurrences of pattern in
    string with repl. {% regex_sub pattern repl string count=0 flags %}
    """
    flags = process_regex_flags(**kwargs)
    return re.sub(
        pattern=pattern, repl=repl, string=string, count=count, flags=flags
    )


@register.simple_tag
def set(value):
    """
    Set a context variable to a specific value.
    """
    return value


@register.filter
def split(obj, separator):
    """
    Return a list of the words in the string, using sep as the delimiter
    string.
    """
    return obj.split(separator)


class SpacelessPlusNode(Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        from django.utils.html import strip_spaces_between_tags
        content = self.nodelist.render(context).strip()
        result = []
        for line in content.split('\n'):
            if line.strip() != '':
                result.append(line)

        return strip_spaces_between_tags(value='\n'.join(result))


@register.tag
def spaceless_plus(parser, token):
    """
    Removes empty lines between the tag nodes.
    """
    nodelist = parser.parse(('endspaceless_plus',))
    parser.delete_first_token()
    return SpacelessPlusNode(nodelist)
