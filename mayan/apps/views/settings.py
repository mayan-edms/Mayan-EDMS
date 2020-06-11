from django.utils.translation import ugettext_lazy as _

from mayan.apps.smart_settings.classes import SettingNamespace

namespace = SettingNamespace(label=_('Views'), name='views')

setting_paginate_by = namespace.add_setting(
    global_name='VIEWS_PAGINATE_BY',
    default=40,
    help_text=_(
        'The number objects that will be displayed per page.'
    )
)
