from django.utils.translation import ugettext_lazy as _

from navigation.api import Link


def is_superuser(context):
    return context['request'].user.is_staff or context['request'].user.is_superuser

formats_list = Link(text=_('file formats'), view='formats_list', sprite='pictures', icon='pictures.png', condition=is_superuser, children_view_regex=[r'formats_list'])
