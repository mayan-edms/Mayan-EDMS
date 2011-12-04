from django.utils.translation import ugettext_lazy as _

PICTURE_ERROR_SMALL = u'picture_error.png'
PICTURE_ERROR_MEDIUM = u'1297211435_error.png'
PICTURE_UNKNOWN_SMALL = u'1299549572_unknown2.png'
PICTURE_UNKNOWN_MEDIUM = u'1299549805_unknown.png'

PERMISSION_DOCUMENT_CREATE = {'namespace': 'documents', 'name': 'document_create', 'label': _(u'Create documents')}
PERMISSION_DOCUMENT_PROPERTIES_EDIT = {'namespace': 'documents', 'name': 'document_properties_edit', 'label': _(u'Edit document properties')}
PERMISSION_DOCUMENT_EDIT = {'namespace': 'documents', 'name': 'document_edit', 'label': _(u'Edit documents')}
PERMISSION_DOCUMENT_VIEW = {'namespace': 'documents', 'name': 'document_view', 'label': _(u'View documents')}
PERMISSION_DOCUMENT_DELETE = {'namespace': 'documents', 'name': 'document_delete', 'label': _(u'Delete documents')}
PERMISSION_DOCUMENT_DOWNLOAD = {'namespace': 'documents', 'name': 'document_download', 'label': _(u'Download documents')}
PERMISSION_DOCUMENT_TRANSFORM = {'namespace': 'documents', 'name': 'document_transform', 'label': _(u'Transform documents')}
PERMISSION_DOCUMENT_TOOLS = {'namespace': 'documents', 'name': 'document_tools', 'label': _(u'Execute document modifying tools')}
PERMISSION_DOCUMENT_VERSION_REVERT = {'namespace': 'documents', 'name': 'document_version_revert', 'label': _(u'Revert documents to a previous version')}

PERMISSION_DOCUMENT_TYPE_EDIT = {'namespace': 'documents_setup', 'name': 'document_type_edit', 'label': _(u'Edit document types')}
PERMISSION_DOCUMENT_TYPE_DELETE = {'namespace': 'documents_setup', 'name': 'document_type_delete', 'label': _(u'Delete document types')}
PERMISSION_DOCUMENT_TYPE_CREATE = {'namespace': 'documents_setup', 'name': 'document_type_create', 'label': _(u'Create document types')}

HISTORY_DOCUMENT_CREATED = {
    'namespace': 'documents', 'name': 'document_created',
    'label': _(u'Document creation'),
    'summary': _(u'Document "%(content_object)s" created by %(fullname)s.'),
    'details': _(u'Document "%(content_object)s" created on %(datetime)s by %(fullname)s.'),
    'expressions': {'fullname': 'user.get_full_name() if user.get_full_name() else user.username'}
}

HISTORY_DOCUMENT_EDITED = {
    'namespace': 'documents', 'name': 'document_edited',
    'label': _(u'Document edited'),
    'summary': _(u'Document "%(content_object)s" edited by %(fullname)s.'),
    'details': _(u'Document "%(content_object)s" was edited on %(datetime)s by %(fullname)s.  The following changes took place: %(changes)s.'),
    'expressions': {
        'fullname': 'user.get_full_name() if user.get_full_name() else user.username',
        'changes': 'u\', \'.join([\'"%s": "%s" -> "%s"\' % (key, value[\'old_value\'], value[\'new_value\']) for key, value in diff.items()])'
    }
}

HISTORY_DOCUMENT_DELETED = {
    'namespace': 'documents', 'name': 'document_deleted',
    'label': _(u'Document deleted'),
    'summary': _(u'Document "%(document)s" deleted by %(fullname)s.'),
    'details': _(u'Document "%(document)s" deleted on %(datetime)s by %(fullname)s.'),
    'expressions': {'fullname': 'user.get_full_name() if user.get_full_name() else user.username'}
}

RELEASE_LEVEL_FINAL = 1
RELEASE_LEVEL_ALPHA = 2
RELEASE_LEVEL_BETA = 3
RELEASE_LEVEL_RC = 4
RELEASE_LEVEL_HF = 5

RELEASE_LEVEL_CHOICES = (
    (RELEASE_LEVEL_FINAL, _(u'final')),
    (RELEASE_LEVEL_ALPHA, _(u'alpha')),
    (RELEASE_LEVEL_BETA, _(u'beta')),
    (RELEASE_LEVEL_RC, _(u'release candidate')),
    (RELEASE_LEVEL_HF, _(u'hotfix')),
)

VERSION_UPDATE_MAJOR = u'major'
VERSION_UPDATE_MINOR = u'minor'
VERSION_UPDATE_MICRO = u'micro'
