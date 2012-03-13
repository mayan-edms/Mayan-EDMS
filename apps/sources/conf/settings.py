"""Configuration options for the sources app"""
import os

from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from smart_settings.api import Setting, SettingNamespace

namespace = SettingNamespace('sources', _(u'Sources'), module='sources.conf.settings')

POP3_DEFAULT_TIMEOUT = 10 # for POP3 only not POP3_SSL
POP3_DEFAULT_EMAIL_PROCESSING_INTERVAL = 60
DEFAULT_POP3_EMAIL_LOG_COUNT = 10 # Max log entries to store

Setting(
    namespace=namespace,
    name='POP3_TIMEOUT',
    global_name='SOURCES_POP3_TIMEOUT',
    default=POP3_DEFAULT_TIMEOUT,
)

Setting(
    namespace=namespace,
    name='POP3_EMAIL_PROCESSING_INTERVAL',
    global_name='SOURCES_POP3_EMAIL_PROCESSING_INTERVAL',
    default=POP3_DEFAULT_EMAIL_PROCESSING_INTERVAL,
)

Setting(
    namespace=namespace,
    name='POP3_EMAIL_LOG_SIZE',
    global_name='SOURCES_POP3_EMAIL_LOG_SIZE',
    default=DEFAULT_POP3_EMAIL_LOG_COUNT,
)
