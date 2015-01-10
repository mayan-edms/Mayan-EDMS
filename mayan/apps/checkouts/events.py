from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from events.classes import Event

event_document_check_out = Event(name='checkouts_document_check_out', label=_('Document checked out'))

HISTORY_DOCUMENT_CHECKED_OUT = {
    'namespace': 'checkouts', 'name': 'document_checked_out',
    'label': _(u'Document checked out'),
    'summary': _(u'Document "%(document)s" checked out by %(fullname)s.'),
    'expressions': {'fullname': 'user.get_full_name() if user.get_full_name() else user'}
}

event_document_check_in = Event(name='checkouts_document_check_in', label=_('Document checked in'))

HISTORY_DOCUMENT_CHECKED_IN = {
    'namespace': 'checkouts', 'name': 'document_checked_in',
    'label': _(u'Document checked in'),
    'summary': _(u'Document "%(document)s" checked in by %(fullname)s.'),
    'expressions': {'fullname': 'user.get_full_name() if user.get_full_name() else user'}
}

event_document_auto_check_in = Event(name='checkouts_document_auto_check_in', label=_('Document automatically checked in'))

HISTORY_DOCUMENT_AUTO_CHECKED_IN = {
    'namespace': 'checkouts', 'name': 'document_auto_checked_in',
    'label': _(u'Document automatically checked in'),
    'summary': _(u'Document "%(document)s" automatically checked in.'),
}

event_document_forceful_check_in = Event(name='checkouts_document_forceful_check_in', label=_('Document forcefully checked in'))

HISTORY_DOCUMENT_FORCEFUL_CHECK_IN = {
    'namespace': 'checkouts', 'name': 'document_forefull_check_in',
    'label': _(u'Document forcefully checked in'),
    'summary': _(u'Document "%(document)s" forcefully checked in by %(fullname)s.'),
    'expressions': {'fullname': 'user.get_full_name() if user.get_full_name() else user'}
}
