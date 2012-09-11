from django.utils.translation import ugettext
from django.utils.safestring import mark_safe
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse


def role_permission_link(requester, permission, permission_list):
    ct = ContentType.objects.get_for_model(requester)

    template = u'<span class="nowrap"><a href="%(url)s">{{ icon.display_small }}%(text)s</a></span>'

    if permission in permission_list:
        return mark_safe(template % {
            'url': reverse('permission_revoke',
                args=[permission.pk, ct.app_label, ct.model, requester.pk]),
            'icon': u'key_delete', 'text': ugettext(u'Revoke')})
    else:
        return mark_safe(template % {
            'url': reverse('permission_grant',
                args=[permission.pk, ct.app_label, ct.model, requester.pk]),
            'icon': u'key_add', 'text': ugettext(u'Grant')})
