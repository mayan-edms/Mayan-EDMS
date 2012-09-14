from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation import Link

from .icons import icon_format_list

def is_superuser(context):
    return context['request'].user.is_staff or context['request'].user.is_superuser

formats_list = Link(text=_('file formats'), view='formats_list', icon=icon_format_list, condition=is_superuser, children_view_regex=[r'formats_list'])
