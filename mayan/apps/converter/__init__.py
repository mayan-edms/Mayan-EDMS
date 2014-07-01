from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation.api import register_sidebar_template
from project_tools.api import register_tool


def is_superuser(context):
    return context['request'].user.is_staff or context['request'].user.is_superuser


formats_list = {'text': _('file formats'), 'view': 'formats_list', 'famfam': 'pictures', 'icon': 'pictures.png', 'condition': is_superuser, 'children_view_regex': [r'formats_list']}

register_sidebar_template(['formats_list'], 'converter_file_formats_help.html')

register_tool(formats_list)
