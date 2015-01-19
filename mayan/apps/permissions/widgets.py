from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext


def role_permission_link(requester, permission, permission_list):
    ct = ContentType.objects.get_for_model(requester)

    template = '<span class="nowrap"><a href="%(url)s"><span class="famfam active famfam-%(icon)s"></span>%(text)s</a></span>'

    if permission in permission_list:
        return mark_safe(template % {
            'url': reverse('permission_revoke',
                           args=[permission.pk, ct.app_label, ct.model,
                           requester.pk]),
            'icon': 'key_delete', 'text': ugettext('Revoke')})
    else:
        return mark_safe(template % {
            'url': reverse('permission_grant',
                           args=[permission.pk, ct.app_label, ct.model,
                           requester.pk]),
            'icon': 'key_add', 'text': ugettext('Grant')})
