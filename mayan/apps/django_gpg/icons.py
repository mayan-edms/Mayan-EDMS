from __future__ import absolute_import, unicode_literals

from mayan.apps.appearance.classes import Icon

icon_key_delete = Icon(driver_name='fontawesome', symbol='times')
icon_key_detail = Icon(driver_name='fontawesome', symbol='key')
icon_key_download = Icon(driver_name='fontawesome', symbol='download')
icon_key_setup = Icon(driver_name='fontawesome', symbol='key')
icon_key_upload = Icon(driver_name='fontawesome', symbol='upload')
icon_keyserver_search = Icon(driver_name='fontawesome', symbol='search')
icon_private_keys = Icon(
    driver_name='fontawesome-dual', primary_symbol='key',
    secondary_symbol='eye-slash'
)
icon_public_keys = Icon(
    driver_name='fontawesome-dual', primary_symbol='key',
    secondary_symbol='eye'
)
