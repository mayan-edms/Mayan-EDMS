import re

from django.conf import settings
from django.template import Library, Node, TemplateSyntaxError
from django.utils.safestring import mark_safe

from web_theme.settings import THEME, ENABLE_SCROLL_JS

register = Library()


class GetThemeNode(Node):
    def __init__(self, var_name, *args):
        self.var_name = var_name

    def render(self, context):
        context['web_theme'] = THEME
        context['enable_scroll_js'] = ENABLE_SCROLL_JS
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
        #TODO: fix properly
        if self.format_string == 'THEME':
            context[self.var_name] = THEME
        else:
            context[self.var_name] = ENABLE_SCROLL_JS
        #context[self.var_name] = getattr(web_theme_settings, self.format_string, '')
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
