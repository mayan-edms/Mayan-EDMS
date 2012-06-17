from django.utils.translation import ugettext_lazy as _

HISTORY_DOCUMENT_CHECKED_OUT = {
    'namespace': 'checkouts', 'name': 'document_checked_out',
    'label': _(u'Document checked out'),
    'summary': _(u'Document "%(document)s" checked out by %(fullname)s.'),
    'expressions': {'fullname': 'user.get_full_name() if user.get_full_name() else user'}
}

HISTORY_DOCUMENT_CHECKED_IN = {
    'namespace': 'checkouts', 'name': 'document_checked_in',
    'label': _(u'Document checked in'),
    'summary': _(u'Document "%(document)s" checked in by %(fullname)s.'),
    'expressions': {'fullname': 'user.get_full_name() if user.get_full_name() else user'}
}
