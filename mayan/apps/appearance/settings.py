from django.utils.translation import ugettext_lazy as _

from mayan.apps.smart_settings.classes import Namespace

from .literals import DEFAULT_MAXIMUM_TITLE_LENGTH, DEFAULT_MESSAGE_POSITION

namespace = Namespace(label=_('Appearance'), name='appearance')

setting_max_title_length = namespace.add_setting(
    default=DEFAULT_MAXIMUM_TITLE_LENGTH,
    global_name='APPEARANCE_MAXIMUM_TITLE_LENGTH', help_text=_(
        'Maximum number of characters that will be displayed as the view '
        'title.'
    )
)
setting_message_position = namespace.add_setting(
    default=DEFAULT_MESSAGE_POSITION,
    global_name='APPEARANCE_MESSAGE_POSITION', help_text=_(
        'Position where the system message will be displayed. Options are: '
        'top-left, top-center, top-right, bottom-left, bottom-center, '
        'bottom-right.'
    )
)
