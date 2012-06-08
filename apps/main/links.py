from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation.api import Link


def is_superuser(context):
    return context['request'].user.is_staff or context['request'].user.is_superuser

maintenance_menu = Link(text=_(u'maintenance'), view='maintenance_menu', sprite='wrench', icon='wrench.png')
statistics = Link(text=_(u'statistics'), view='statistics', sprite='table', icon='blackboard_sum.png', condition=is_superuser, children_view_regex=[r'statistics'])
diagnostics = Link(text=_(u'diagnostics'), view='diagnostics', sprite='pill', icon='pill.png')
sentry = Link(text=_(u'sentry'), view='sentry', sprite='bug', icon='bug.png', condition=is_superuser)
admin_site = Link(text=_(u'admin site'), view='admin:index', sprite='keyboard', icon='keyboard.png', condition=is_superuser)
