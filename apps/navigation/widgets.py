from django.utils.safestring import mark_safe
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.template.defaultfilters import capfirst
from django.core.exceptions import PermissionDenied

from permissions.api import check_permissions


def button_navigation_widget(request, link):
    if 'permissions' in link:
        try:
            check_permissions(request.user, link['permissions'])
            return render_widget(link)
        except PermissionDenied:
            return u''
    else:
        return render_widget(link)

 
def render_widget(link):
    return mark_safe(u'<a style="text-decoration:none; margin-right: 10px;" href="%(url)s"><button style="vertical-align: top; padding: 1px; width: 110px; height: 100px; margin: 10px;"><img src="%(static_url)simages/icons/%(icon)s" alt="%(image_alt)s" /><p style="margin: 0px 0px 0px 0px;">%(string)s</p></button></a>' % {
        'url': reverse(link['view']) if 'view' in link else link['url'],
        'icon': link.get('icon', 'link_button.png'),
        'static_url': settings.STATIC_URL,
        'string': capfirst(link['text']),
        'image_alt': _(u'icon'),
    })
