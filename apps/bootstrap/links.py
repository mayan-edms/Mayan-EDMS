from django.utils.translation import ugettext_lazy as _


def is_superuser(context):
    return context['request'].user.is_staff or context['request'].user.is_superuser


database_bootstrap = {'text': _(u'bootstrap database'), 'view': 'bootstrap_type_list', 'icon': 'database_lightning.png', 'condition': is_superuser}#, 'children_view_regex': [r'statistics']}
bootstrap_execute = {'text': _(u'execute'), 'view': 'bootstrap_execute', 'args': 'object.name', 'sprite': 'database_lightning.png', 'condition': is_superuser}#, 'children_view_regex': [r'statistics']}
