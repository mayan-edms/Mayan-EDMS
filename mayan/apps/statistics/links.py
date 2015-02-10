from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _


def is_superuser(context):
    return context['request'].user.is_staff or context['request'].user.is_superuser


link_execute = {'text': _('Execute'), 'view': 'statistics:execute', 'args': 'object.id', 'famfam': 'lightning', 'condition': is_superuser}
link_namespace_details = {'text': _('Details'), 'view': 'statistics:namespace_details', 'args': 'namespace.id', 'famfam': 'chart_curve_go', 'condition': is_superuser}
link_namespace_list = {'text': _('Namespace list'), 'view': 'statistics:namespace_list', 'famfam': 'chart_curve', 'condition': is_superuser}
link_statistics = {'text': _('Statistics'), 'view': 'statistics:namespace_list', 'famfam': 'table', 'icon': 'main/icons/blackboard_sum.png', 'condition': is_superuser}
