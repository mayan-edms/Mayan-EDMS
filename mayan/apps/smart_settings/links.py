from django.utils.translation import ugettext_lazy as _


def is_superuser(context):
    return context['request'].user.is_staff or context['request'].user.is_superuser


check_settings = {'text': _(u'Settings'), 'view': 'settings:setting_list', 'famfam': 'cog', 'icon': 'cog.png', 'condition': is_superuser}
