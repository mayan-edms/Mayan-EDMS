from django.utils.translation import ugettext_lazy as _


def is_superuser(context):
    return context['request'].user.is_staff or context['request'].user.is_superuser


maintenance_menu = {'text': _(u'Maintenance'), 'view': 'main:maintenance_menu', 'famfam': 'wrench', 'icon': 'wrench.png'}
admin_site = {'text': _(u'Admin site'), 'view': 'admin:index', 'famfam': 'keyboard', 'icon': 'keyboard.png', 'condition': is_superuser}
