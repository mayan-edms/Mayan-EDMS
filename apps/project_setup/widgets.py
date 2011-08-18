from django.utils.safestring import mark_safe
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.template.defaultfilters import capfirst
from django.core.exceptions import PermissionDenied

from permissions.api import check_permissions


def setup_button_widget(request, setup_link):
    if 'permissions' in setup_link:
        try:
            check_permissions(request.user, setup_link['permissions'])
            return render_widget(setup_link)
        except PermissionDenied:
            return u''
    else:
        return render_widget(setup_link)

 
def render_widget(setup_link):
    return mark_safe(u'<a style="text-decoration:none; margin-right: 10px;" href="%(url)s"><button style="vertical-align: top; padding: 1px; width: 110px; height: 100px; margin: 10px;"><img src="%(static_url)simages/icons/%(icon)s" alt="%(image_alt)s" /><p style="margin: 0px 0px 0px 0px;">%(string)s</p></button></a>' % {
        'url': reverse(setup_link['view']) if 'view' in setup_link else setup_link['url'],
        'icon': setup_link.get('icon', 'link_button.png'),
        'static_url': settings.STATIC_URL,
        'string': capfirst(setup_link['text']),
        'image_alt': _(u'icon'),
    })
