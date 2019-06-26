from __future__ import absolute_import, unicode_literals

from mayan.apps.appearance.classes import Icon

icon_redaction_create = Icon(
    driver_name='fontawesome-dual', primary_symbol='highlighter',
    secondary_symbol='plus'
)
icon_redaction_delete = Icon(driver_name='fontawesome', symbol='times')
icon_redaction_edit = Icon(driver_name='fontawesome', symbol='pencil-alt')
icon_redactions = Icon(driver_name='fontawesome', symbol='highlighter')
