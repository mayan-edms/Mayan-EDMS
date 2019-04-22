from __future__ import absolute_import, unicode_literals

from mayan.apps.appearance.classes import Icon

icon_transformation = Icon(driver_name='fontawesome', symbol='crop')
icon_transformation_create = Icon(
    driver_name='fontawesome-dual', primary_symbol='crop',
    secondary_symbol='plus'
)
icon_transformation_delete = Icon(driver_name='fontawesome', symbol='times')
icon_transformation_edit = Icon(driver_name='fontawesome', symbol='pencil-alt')
