from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from mayan.apps.navigation.classes import Link

link_redaction_create = Link(
    icon_class_path='mayan.apps.redactions.icons.icon_redaction_create',
    #permissions=(,), text=_('Redactions'),
    text=_('Add redaction'),
    view='redactions:redaction_create', args='resolved_object.id'
)
link_redaction_edit = Link(
    #icon_class_path='mayan.apps.redactions.icons.icon_redaction_create',
    #permissions=(,), text=_('Redactions'),
    text=_('Edit'),
    view='redactions:redaction_edit', args='resolved_object.id'
)
link_redaction_list = Link(
    icon_class_path='mayan.apps.redactions.icons.icon_redactions',
    #permissions=(,), text=_('Redactions'),
    text=_('Redactions'),
    view='redactions:redaction_list', args='resolved_object.id'
)

