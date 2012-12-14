from django.utils.translation import ugettext_lazy as _

from history.api import EventNamespace, Event

namespace = EventNamespace('documents', _('documents'))

history_document_created = Event(namespace=namespace, name='document_created', label=_(u'Document creation'),
    summary=_(u'Document "%(content_object)s" created by %(fullname)s.'),
    details=_(u'Document "%(content_object)s" created on %(datetime)s by %(fullname)s.'),
    expressions={'fullname': 'user.get_full_name() if user.get_full_name() else user.username'}
)

history_document_edited = Event(namespace=namespace, name='document_edited', label=_(u'Document edited'),
    summary=_(u'Document "%(content_object)s" edited by %(fullname)s.'),
    details=_(u'Document "%(content_object)s" was edited on %(datetime)s by %(fullname)s.  The following changes took place: %(changes)s.'),
    expressions={
        'fullname': 'user.get_full_name() if user.get_full_name() else user.username',
        'changes': 'u\', \'.join([\'"%s": "%s" -> "%s"\' % (key, value[\'old_value\'], value[\'new_value\']) for key, value in diff.items()])'
    }
)

history_document_deleted = Event(namespace=namespace, name='document_deleted', label=_(u'Document deleted'),
    summary=_(u'Document "%(document)s" deleted by %(fullname)s.'),
    details=_(u'Document "%(document)s" deleted on %(datetime)s by %(fullname)s.'),
    expressions={'fullname': 'user.get_full_name() if user.get_full_name() else user.username'}
)
