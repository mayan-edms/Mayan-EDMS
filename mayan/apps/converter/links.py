from django.utils.translation import ugettext_lazy as _


def is_superuser(context):
    return context['request'].user.is_staff or context['request'].user.is_superuser


formats_list = {'text': _('file formats'), 'view': 'converter:formats_list', 'famfam': 'pictures', 'icon': 'pictures.png', 'condition': is_superuser, 'children_view_regex': [r'formats_list']}
