from django.utils.translation import ugettext_lazy as _


def is_superuser(context):
    return context['request'].user.is_staff or context['request'].user.is_superuser


maintenance_menu = {'text': _(u'maintenance'), 'view': 'maintenance_menu', 'famfam': 'wrench', 'icon': 'wrench.png'}
diagnostics = {'text': _(u'diagnostics'), 'view': 'diagnostics', 'famfam': 'pill', 'icon': 'pill.png'}
sentry = {'text': _(u'sentry'), 'view': 'sentry', 'famfam': 'bug', 'icon': 'bug.png', 'condition': is_superuser}
admin_site = {'text': _(u'admin site'), 'view': 'admin:index', 'famfam': 'keyboard', 'icon': 'keyboard.png', 'condition': is_superuser}
