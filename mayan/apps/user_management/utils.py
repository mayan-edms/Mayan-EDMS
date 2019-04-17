from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _


def get_user_label_text(context):
    if not context['request'].user.is_authenticated:
        return _('Anonymous')
    else:
        return context['request'].user.get_full_name() or context['request'].user
