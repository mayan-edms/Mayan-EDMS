from django.utils.translation import ugettext_lazy as _

from mayan.apps.smart_settings.classes import SettingNamespace

from .literals import (
    DEFAULT_VIEWS_PAGINATE_BY, DEFAULT_VIEWS_PAGING_ARGUMENT
)

namespace = SettingNamespace(label=_('Views'), name='views')

setting_paginate_by = namespace.add_setting(
    default=DEFAULT_VIEWS_PAGINATE_BY, global_name='VIEWS_PAGINATE_BY',
    help_text=_(
        'The number objects that will be displayed per page.'
    )
)
setting_paging_argument = namespace.add_setting(
    default=DEFAULT_VIEWS_PAGING_ARGUMENT,
    global_name='VIEWS_PAGING_ARGUMENT',
    help_text=_(
        'A string specifying the name to use for the paging parameter.'
    )
)
