from __future__ import absolute_import

import urlparse

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.template import RequestContext, Variable
from django.template.defaultfilters import capfirst
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from permissions.models import Permission

from .templatetags.navigation_tags import resolve_links
from .utils import resolve_to_name


def button_navigation_widget(request, link):
    if 'permissions' in link:
        try:
            Permission.objects.check_permissions(request.user, link['permissions'])
            return render_widget(request, link)
        except PermissionDenied:
            return u''
    else:
        return render_widget(request, link)


def render_widget(request, link):
    context = RequestContext(request)

    request = Variable('request').resolve(context)
    current_path = request.META['PATH_INFO']
    current_view = resolve_to_name(current_path)

    query_string = urlparse.urlparse(request.get_full_path()).query or urlparse.urlparse(request.META.get('HTTP_REFERER', u'/')).query
    parsed_query_string = urlparse.parse_qs(query_string)

    links = resolve_links(context, [link], current_view, current_path, parsed_query_string)
    if links:
        link = links[0]
        return mark_safe(u'<a style="text-decoration:none; margin-right: 10px;" href="%(url)s"><button style="vertical-align: top; padding: 1px; width: 110px; height: 100px; margin: 10px;"><img src="%(static_url)simages/icons/%(icon)s" alt="%(image_alt)s" /><p style="margin: 0px 0px 0px 0px;">%(string)s</p></button></a>' % {
            'url': reverse(link['view']) if 'view' in link else link['url'],
            'icon': link.get('icon', 'link_button.png'),
            'static_url': settings.STATIC_URL,
            'string': capfirst(link['text']),
            'image_alt': _(u'icon'),
        })
    else:
        return u''
