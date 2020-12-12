from django.utils.translation import ugettext_lazy as _

from mayan.apps.smart_settings.classes import SettingNamespace

from .literals import DEFAULT_EMAIL, DEFAULT_PASSWORD, DEFAULT_USERNAME

namespace = SettingNamespace(label=_('Auto administrator'), name='autoadmin')

setting_email = namespace.add_setting(
    default=DEFAULT_EMAIL, global_name='AUTOADMIN_EMAIL', help_text=_(
        'Sets the email of the automatically created super user account.'
    )
)
setting_password = namespace.add_setting(
    default=DEFAULT_PASSWORD, global_name='AUTOADMIN_PASSWORD', help_text=_(
        'The password of the automatically created super user account. '
        'If it is equal to None, the password is randomly generated.'
    )
)
setting_username = namespace.add_setting(
    default=DEFAULT_USERNAME, global_name='AUTOADMIN_USERNAME', help_text=_(
        'The username of the automatically created super user account.'
    )
)
