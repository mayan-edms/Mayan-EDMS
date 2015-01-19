from __future__ import unicode_literals

from django.conf import settings
from django.core.urlresolvers import reverse
from django.template import Library, Node
from django.utils.safestring import mark_safe

register = Library()


class LoginRedirectNode(Node):
    def render(self, context):
        context['LOGIN_REDIRECT_URL'] = getattr(settings, 'LOGIN_REDIRECT_URL', reverse('main:home'))
        return ''


@register.tag
def get_login_redirect_url(parser, token):
    return LoginRedirectNode()


@register.filter
def highlight(text, word):
    return mark_safe(unicode(text).replace(word, mark_safe('<mark>%s</mark>' % word)))
