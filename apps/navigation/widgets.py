from __future__ import absolute_import

from django.utils.safestring import mark_safe
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import capfirst
from django.core.exceptions import PermissionDenied
from django.template import RequestContext

from icons.api import get_icon_name, get_sprite_name
from icons.literals import ERROR
from permissions.models import Permission


def button_navigation_widget(request, link):
    if link.permissions:
        try:
            Permission.objects.check_permissions(request.user, link.permissions)
            return render_widget(request, link)
        except PermissionDenied:
            return u''
    else:
        return render_widget(request, link)


def render_widget(request, link):
    context = RequestContext(request)
    resolved_link = link.resolve(context)
    if resolved_link:
        return mark_safe(u'<a style="text-decoration:none; margin-right: 10px;" href="%(url)s"><button style="vertical-align: top; padding: 1px; width: 110px; height: 100px; margin: 10px;"><img src="%(static_url)simages/icons/%(icon)s" alt="%(image_alt)s" /><p style="margin: 0px 0px 0px 0px;">%(string)s</p></button></a>' % {
            'url': resolved_link.url,
            'icon': get_icon_name(getattr(resolved_link, 'icon', ERROR)),
            'static_url': settings.STATIC_URL,
            'string': capfirst(resolved_link.text),
            'image_alt': _(u'icon'),
        })
    else:
        return u''
