from django.utils.translation import ugettext_lazy as _

from project_setup.api import register_setup


def is_superuser(context):
    return context['request'].user.is_staff or context['request'].user.is_superuser

check_settings = {'text': _(u'settings'), 'view': 'setting_list', 'famfam': 'cog', 'icon': 'cog.png', 'condition': is_superuser, 'children_view_regex': [r'^setting_']}

register_setup(check_settings)
