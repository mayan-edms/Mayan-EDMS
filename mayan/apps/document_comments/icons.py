from __future__ import absolute_import, unicode_literals

from mayan.apps.appearance.classes import Icon

icon_comment_add = Icon(
    driver_name='fontawesome-dual', primary_symbol='comment',
    secondary_symbol='plus'
)
icon_comment_delete = Icon(driver_name='fontawesome', symbol='times')
icon_comments_for_document = Icon(driver_name='fontawesome', symbol='comment')
