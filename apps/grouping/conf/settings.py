"""Configuration options for the grouping app"""

from smart_settings.api import register_settings

register_settings(
    namespace=u'grouping',
    module=u'grouping.conf.settings',
    settings=[
        {'name': u'SHOW_EMPTY_GROUPS', 'global_name': u'GROUPING_SHOW_EMPTY_GROUPS', 'default': True},
    ]
)
