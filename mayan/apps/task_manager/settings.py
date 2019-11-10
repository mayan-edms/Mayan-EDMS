from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from mayan.apps.smart_settings.classes import Namespace

# Don't import anything on star import, we just want to make it easy
# for apps.py to activate the settings in this module.
__all__ = ()
namespace = Namespace(label=_('Celery'), name='celery')

setting_celery_broker_url = namespace.add_setting(
    global_name='CELERY_BROKER_URL', default=None,
    help_text=_(
        'Default: "amqp://". Default broker URL. This must be a URL in '
        'the form of: transport://userid:password@hostname:port/virtual_host '
        'Only the scheme part (transport://) is required, the rest is '
        'optional, and defaults to the specific transports default values.'
    ),
)
setting_celery_result_backend = namespace.add_setting(
    global_name='CELERY_RESULT_BACKEND', default=None,
    help_text=_(
        'Default: No result backend enabled by default. The backend used '
        'to store task results (tombstones). Refer to '
        'http://docs.celeryproject.org/en/v4.1.0/userguide/configuration.'
        'html#result-backend'
    )
)
