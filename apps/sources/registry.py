from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from .icons import icon_source_list
from .links import setup_sources
from .cleanup import cleanup

label = _(u'Sources')
description = _(u'Provides source from where to add documents.')
dependencies = ['app_registry', 'icons', 'navigation', 'documents']
icon = icon_source_list
setup_links = [setup_sources]
cleanup_functions = [cleanup]

'''
Setting(
    namespace=namespace,
    name='POP3_TIMEOUT',
    global_name='SOURCES_POP3_TIMEOUT',
    default=POP3_DEFAULT_TIMEOUT,
)

Setting(
    namespace=namespace,
    name='EMAIL_PROCESSING_INTERVAL',
    global_name='SOURCES_EMAIL_PROCESSING_INTERVAL',
    default=DEFAULT_EMAIL_PROCESSING_INTERVAL,
)

Setting(
    namespace=namespace,
    name='LOG_SIZE',
    global_name='SOURCES_LOG_SIZE',
    default=DEFAULT_POP3_EMAIL_LOG_COUNT,
)
'''
