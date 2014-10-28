from django.utils.translation import ugettext_lazy as _

HISTORY_DOCUMENT_CREATED = {
    'namespace': 'documents', 'name': 'document_created',
    'label': _(u'Document creation'),
    'summary': _(u'Document "%(content_object)s" created by %(fullname)s.'),
    'details': _(u'Document "%(content_object)s" created on %(datetime)s by %(fullname)s.'),
    'expressions': {'fullname': 'user[0]["fields"]["username"] if isinstance(user, list) else user.get_full_name() if user.get_full_name() else user.username'}
}

HISTORY_DOCUMENT_EDITED = {
    'namespace': 'documents', 'name': 'document_edited',
    'label': _(u'Document edited'),
    'summary': _(u'Document "%(content_object)s" edited by %(fullname)s.'),
    'details': _(u'Document "%(content_object)s" was edited on %(datetime)s by %(fullname)s.'),
    'expressions': {
        'fullname': 'user[0]["fields"]["username"] if isinstance(user, list) else user.get_full_name() if user.get_full_name() else user.username',
    }
}

HISTORY_DOCUMENT_DELETED = {
    'namespace': 'documents', 'name': 'document_deleted',
    'label': _(u'Document deleted'),
    'summary': _(u'Document "%(document)s" deleted by %(fullname)s.'),
    'details': _(u'Document "%(document)s" deleted on %(datetime)s by %(fullname)s.'),
    'expressions': {'fullname': 'user.get_full_name() if user.get_full_name() else user.username'}
}
