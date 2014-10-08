from __future__ import absolute_import

import re

from django.conf import settings
from django.template import Library, Node, TemplateSyntaxError
from django.utils.safestring import mark_safe

from main import settings as web_theme_settings

register = Library()


class LoginRedirectNode(Node):
    def render(self, context):
        context['LOGIN_REDIRECT_URL'] = getattr(settings, 'LOGIN_REDIRECT_URL', '/')
        return ''


@register.tag
def get_login_redirect_url(parser, token):
    return LoginRedirectNode()


@register.filter
def highlight(text, word):
    return mark_safe(unicode(text).replace(word, mark_safe('<mark>%s</mark>' % word)))
