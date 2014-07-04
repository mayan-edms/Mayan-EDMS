from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _


def is_superuser(context):
    return context['request'].user.is_staff or context['request'].user.is_superuser


link_execute = {'text': _(u'execute'), 'view': 'statistics:execute', 'args': 'object.id', 'famfam': 'lightning', 'condition': is_superuser}
link_namespace_details = {'text': _(u'details'), 'view': 'statistics:namespace_details', 'args': 'namespace.id', 'famfam': 'chart_curve_go', 'condition': is_superuser}
link_namespace_list = {'text': _(u'namespace list'), 'view': 'statistics:namespace_list', 'famfam': 'chart_curve', 'condition': is_superuser, 'children_view_regex': [r'statistics']}
link_statistics = {'text': _(u'Statistics'), 'view': 'statistics:namespace_list', 'famfam': 'table', 'icon': 'blackboard_sum.png', 'condition': is_superuser, 'children_view_regex': [r'statistics']}
