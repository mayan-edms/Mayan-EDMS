from django.utils.translation import ugettext_lazy as _

from mayan.apps.smart_settings.classes import SettingNamespace

from .literals import (
    DEFAULT_CELERY_BROKER_LOGIN_METHOD, DEFAULT_CELERY_BROKER_URL,
    DEFAULT_CELERY_BROKER_USE_SSL, DEFAULT_CELERY_RESULT_BACKEND
)

namespace = SettingNamespace(label=_('Celery'), name='celery')

setting_celery_broker_login_method = namespace.add_setting(
    default=DEFAULT_CELERY_BROKER_LOGIN_METHOD,
    global_name='CELERY_BROKER_LOGIN_METHOD', help_text=_(
        'Default: "AMQPLAIN". Set custom amqp login method.'
    )
)
setting_celery_broker_url = namespace.add_setting(
    default=DEFAULT_CELERY_BROKER_URL, global_name='CELERY_BROKER_URL',
    help_text=_(
        'Default: "amqp://". Default broker URL. This must be a URL in '
        'the form of: transport://userid:password@hostname:port/virtual_host '
        'Only the scheme part (transport://) is required, the rest is '
        'optional, and defaults to the specific transports default values.'
    )
)
setting_celery_broker_use_ssl = namespace.add_setting(
    default=DEFAULT_CELERY_BROKER_USE_SSL,
    global_name='CELERY_BROKER_USE_SSL', help_text=_(
        'Default: "Disabled". Toggles SSL usage on broker connection '
        'and SSL settings. The valid values for this option vary by '
        'transport.'
    )
)
setting_celery_result_backend = namespace.add_setting(
    default=DEFAULT_CELERY_RESULT_BACKEND,
    global_name='CELERY_RESULT_BACKEND', help_text=_(
        'Default: No result backend enabled by default. The backend used '
        'to store task results (tombstones). Refer to '
        'http://docs.celeryproject.org/en/v4.1.0/userguide/configuration.'
        'html#result-backend'
    )
)
