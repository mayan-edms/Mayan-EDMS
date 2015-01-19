from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from events.classes import Event

event_document_create = Event(name='documents_document_create', label=_('Document created'))
event_document_properties_edit = Event(name='documents_document_edit', label=_('Document properties edited'))
event_document_type_change = Event(name='documents_document_type_change', label=_('Document type changed'))
