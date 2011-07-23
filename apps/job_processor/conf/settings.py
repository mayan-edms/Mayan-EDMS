"""Configuration options for the job_processing app"""
from django.utils.translation import ugettext_lazy as _

from smart_settings.api import register_settings

register_settings(
    namespace=u'job_processor',
    module=u'job_processor.conf.settings',
    settings=[
        {'name': u'BACKEND', 'global_name': u'JOB_PROCESSING_BACKEND', 'default': None, 'description': _('Specified which job processing library to use, option are: None and celery.')},
    ]
)
