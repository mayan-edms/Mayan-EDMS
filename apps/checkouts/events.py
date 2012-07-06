from django.utils.translation import ugettext_lazy as _

from history.api import EventNamespace, Event

namespace = EventNamespace('checkouts', _(u'checkouts'))

history_document_checked_out = Event(namespace=namespace, name='document_checked_out', label=_(u'Document checked out'),
    summary=_(u'Document "%(document)s" checked out by %(fullname)s.'),
    expressions={'fullname': 'user.get_full_name() if user.get_full_name() else user'}
)

history_document_checked_in = Event(namespace=namespace, name='document_checked_in', label=_(u'Document checked in'),
    summary=_(u'Document "%(document)s" checked in by %(fullname)s.'),
    expressions={'fullname': 'user.get_full_name() if user.get_full_name() else user'}
)

history_document_auto_checked_in = Event(namespace=namespace, name='document_auto_checked_in', label=_(u'Document automatically checked in'),
    summary=_(u'Document "%(document)s" automatically checked in.'),
)

history_document_forceful_check_in = Event(namespace=namespace, name='document_forefull_check_in', label=_(u'Document forcefully checked in'),
    summary=_(u'Document "%(document)s" forcefully checked in by %(fullname)s.'),
    expressions={'fullname': 'user.get_full_name() if user.get_full_name() else user'}
)
