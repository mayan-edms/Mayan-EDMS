from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation import Link

from .icons import icon_statistics


def is_superuser(context):
    return context['request'].user.is_staff or context['request'].user.is_superuser


statistics_link = Link(text=_(u'statistics'), view='statistics', icon=icon_statistics, condition=is_superuser, children_view_regex=[r'statistics'])
