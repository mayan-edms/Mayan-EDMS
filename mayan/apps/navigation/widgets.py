from __future__ import absolute_import

import urlparse

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.template import RequestContext, Variable
from django.utils.safestring import mark_safe
from django.contrib.staticfiles.storage import staticfiles_storage
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

    query_string = urlparse.urlparse(request.get_full_path()).query or urlparse.urlparse(request.META.get('HTTP_REFERER', reverse('main:home'))).query
    parsed_query_string = urlparse.parse_qs(query_string)

    links = resolve_links(context, [link], current_view, current_path, parsed_query_string)
    if links:
        link = links[0]
        return mark_safe(u'\
            <a class="pure-button mayan-button-big" href="%(url)s">\
                <p>\
                    <img src="%(static_url)s"><br>\
                    %(string)s\
                </p>\
            </a>' % {
            'url': reverse(link['view']) if 'view' in link else link['url'],
            'static_url': staticfiles_storage.url('main/icons/{0}'.format(link.get('icon', 'link_button.png'))),
            'string': link['text'],
            'image_alt': _(u'Icon'),
        })
    else:
        return u''
