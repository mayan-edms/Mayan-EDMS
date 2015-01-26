from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _


def is_superuser(context):
    return context['request'].user.is_staff or context['request'].user.is_superuser


check_settings = {'text': _('Settings'), 'view': 'settings:setting_list', 'famfam': 'cog', 'icon': 'main/icons/cog.png', 'condition': is_superuser}
