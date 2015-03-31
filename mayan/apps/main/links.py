from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _


def is_superuser(context):
    return context['request'].user.is_staff or context['request'].user.is_superuser


maintenance_menu = {'text': _('Maintenance'), 'view': 'main:maintenance_menu', 'icon': 'fa fa-wrench'}
admin_site = {'text': _('Admin site'), 'view': 'admin:index', 'icon': 'fa fa-keyboard-o', 'condition': is_superuser}
