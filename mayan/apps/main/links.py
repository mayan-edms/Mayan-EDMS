from django.utils.translation import ugettext_lazy as _


def is_superuser(context):
    return context['request'].user.is_staff or context['request'].user.is_superuser


maintenance_menu = {'text': _(u'Maintenance'), 'view': 'main:maintenance_menu', 'famfam': 'wrench', 'icon': 'wrench.png'}
diagnostics = {'text': _(u'Diagnostics'), 'view': 'main:diagnostics', 'famfam': 'pill', 'icon': 'pill.png'}
sentry = {'text': _(u'Sentry'), 'view': 'main:sentry', 'famfam': 'bug', 'icon': 'bug.png', 'condition': is_superuser}
admin_site = {'text': _(u'Admin site'), 'view': 'admin:index', 'famfam': 'keyboard', 'icon': 'keyboard.png', 'condition': is_superuser}
