"""Configuration options for the filesystem_serving app"""

from main.api import register_settings

register_settings(
    namespace=u'filesystem_serving',
    module=u'filesystem_serving.conf.settings',
    settings=[
        {'name': u'SLUGIFY_PATHS', 'global_name': u'FILESYSTEM_SLUGIFY_PATHS', 'default': False},
        {'name': u'MAX_RENAME_COUNT', 'global_name': u'FILESYSTEM_MAX_RENAME_COUNT', 'default': 200},
        {'name': u'FILESERVING_PATH', 'global_name': u'FILESYSTEM_FILESERVING_PATH', 'default': u'/tmp/mayan/documents', 'exists': True},
        {'name': u'FILESERVING_ENABLE', 'global_name': u'FILESYSTEM_FILESERVING_ENABLE', 'default': True}
    ]
)

