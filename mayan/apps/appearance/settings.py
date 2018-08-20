from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from smart_settings import Namespace

from .literals import DEFAULT_MAXIMUM_TITLE_LENGTH

namespace = Namespace(name='appearance', label=_('Appearance'))
setting_max_title_length = namespace.add_setting(
    default=DEFAULT_MAXIMUM_TITLE_LENGTH,
    global_name='APPEARANCE_MAXIMUM_TITLE_LENGTH', help_text=_(
        'Maximum number of characters that will be displayed as the view '
        'title.'
    )
)
