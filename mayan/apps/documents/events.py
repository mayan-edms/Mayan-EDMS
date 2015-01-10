from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from events.classes import Event

event_document_create = Event(name='documents_document_create', label=_('Document created'))

HISTORY_DOCUMENT_CREATED = {
    'namespace': 'documents', 'name': 'document_created',
    'label': _(u'Document creation'),
    'summary': _(u'Document "%(content_object)s" created by %(fullname)s.'),
    'details': _(u'Document "%(content_object)s" created on %(datetime)s by %(fullname)s.'),
    'expressions': {'fullname': 'user[0]["fields"]["username"] if isinstance(user, list) else user.get_full_name() if user.get_full_name() else user.username'}
}

event_document_edited = Event(name='documents_document_edit', label=_('Document edited'))

HISTORY_DOCUMENT_EDITED = {
    'namespace': 'documents', 'name': 'document_edited',
    'label': _(u'Document edited'),
    'summary': _(u'Document "%(content_object)s" edited by %(fullname)s.'),
    'details': _(u'Document "%(content_object)s" was edited on %(datetime)s by %(fullname)s.'),
    'expressions': {
        'fullname': 'user[0]["fields"]["username"] if isinstance(user, list) else user.get_full_name() if user.get_full_name() else user.username',
    }
}
