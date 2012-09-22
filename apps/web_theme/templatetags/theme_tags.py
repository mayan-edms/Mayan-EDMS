import re

from django.conf import settings
from django.template import Library, Node, TemplateSyntaxError
from django.utils.safestring import mark_safe

from web_theme import settings as web_theme_settings

register = Library()


class GetThemeNode(Node):
    def __init__(self, var_name, *args):
        self.var_name = var_name

    def render(self, context):
        context['web_theme'] = web_theme_settings.THEME
        context['enable_scroll_js'] = web_theme_settings.ENABLE_SCROLL_JS
        return ''


@register.tag
def get_theme(parser, token):
    try:
        # Splitting by None == splitting by spaces.
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise TemplateSyntaxError('%r tag requires arguments' % token.contents.split()[0])

    #m = re.search(r'(.*?) as (\w+)', arg)
    m = re.search(r'as (\w+)', arg)
    if not m:
        raise TemplateSyntaxError('%r tag had invalid arguments' % tag_name)
    #format_string, var_name = m.groups()
    var_name = m.groups()

    #if not (format_string[0] == format_string[-1] and format_string[0] in ('"', "'")):
    #    raise template.TemplateSyntaxError, "%r tag's argument should be in quotes" % tag_name
    return GetThemeNode(var_name)


class LoginRedirectNode(Node):
    def render(self, context):
        context['LOGIN_REDIRECT_URL'] = getattr(settings, 'LOGIN_REDIRECT_URL', '/')
        return ''


@register.tag
def get_login_redirect_url(parser, token):
    return LoginRedirectNode()


class SettingsNode(Node):
    def __init__(self, format_string, var_name):
        self.format_string = format_string
        self.var_name = var_name

    def render(self, context):
        context[self.var_name] = getattr(web_theme_settings, self.format_string, '')
        return ''


@register.tag
def get_web_theme_setting(parser, token):
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


@register.filter
def highlight(text, word):
    #return mark_safe(unicode(text).replace(word, mark_safe('<span class="highlight">%s</span>' % word)))
    return mark_safe(unicode(text).replace(word, mark_safe('<mark>%s</mark>' % word)))
