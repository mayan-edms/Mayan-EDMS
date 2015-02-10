from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _


def is_superuser(context):
    return context['request'].user.is_staff or context['request'].user.is_superuser


maintenance_menu = {'text': _('Maintenance'), 'view': 'main:maintenance_menu', 'famfam': 'wrench', 'icon': 'main/icons/wrench.png'}
admin_site = {'text': _('Admin site'), 'view': 'admin:index', 'famfam': 'keyboard', 'icon': 'main/icons/keyboard.png', 'condition': is_superuser}
